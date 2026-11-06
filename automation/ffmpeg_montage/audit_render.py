#!/usr/bin/env python3
"""Audit a historical saved command against its original export passport.

Never encodes media, calls YouTube, transfers user acceptance, or edits an old
receipt. An explicit --bind-receipt writes a new receipt only after settings pass
and an evidence file is supplied. Absent provenance is not a defect verdict.
"""
import argparse
import copy
import json
import subprocess
from pathlib import Path
import delivery


def audit(receipt_path, passport_path, command_path, prepared_path, work, evidence=None):
    receipt = json.loads(Path(receipt_path).read_text())
    if receipt.get('schema') not in (delivery.SCHEMA, delivery.RECEIPT_SCHEMA):
        raise ValueError('Unsupported receipt schema')
    delivery.check_record(receipt['media'])
    for record in receipt['inputs']:
        delivery.check_record(record)
    contract = receipt['subtitles']
    for record in contract['profiles'] + [contract['audio']['audio'], contract['audio']['speed_evidence'],
                                          contract['audio']['speed_policy'], contract['transcript'], contract['word_map']]:
        delivery.check_record(record)
    prepared = json.loads(Path(prepared_path).read_text())
    manifest = receipt['inputs'][0]['path']
    plan = json.loads(Path(manifest).read_text())
    prepared['source_transfer'] = plan.get('source_transfer')
    if not prepared.get('manifest_path') or Path(prepared['manifest_path']).resolve() != Path(manifest).resolve():
        raise ValueError('Prepared plan identifies another manifest')
    argv = json.loads(Path(command_path).read_text())
    passport = json.loads(Path(passport_path).read_text())
    audio = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','a:0',
        '-show_entries','stream=codec_name,profile,channels,sample_rate,bit_rate','-of','json',prepared['audio']]))['streams'][0]
    settings = delivery.check_export_settings(passport, argv, prepared, audio, manifest, receipt['media']['path'])
    work = Path(work)
    work.mkdir(parents=True, exist_ok=False)
    def snapshot(path, name):
        target = work/name
        target.write_bytes(Path(path).read_bytes())
        result = {'original':delivery.file_record(path), 'snapshot':delivery.file_record(target)}
        if result['original']['sha256'] != result['snapshot']['sha256']:
            raise ValueError('Historical evidence changed during audit')
        return result
    render = {'schema':'ytv-render-v1', 'origin':'historical_command_audit',
              'export_contract':snapshot(passport_path,'export_contract.json'),
              'command':snapshot(command_path,'render_command.json'),
              'engine':[{'original':item} for item in contract['engine']],
              'prepared':prepared, 'audio_source':audio, 'settings':settings,
              'ffmpeg_version':'UNVERIFIED: historical version; current ffprobe only inspected the unchanged source'}
    result = {'status':'SETTINGS_PASS', 'scope':settings['scope'], 'media':receipt['media'],
              'source_receipt':delivery.file_record(receipt_path), 'render':render,
              'limitations':['No AV QA; no user acceptance inferred; historical engine hashes retained without fabricating source snapshots.']}
    if evidence is not None:
        render['audit_evidence'] = delivery.file_record(evidence)
        delivery.validate_render_binding(render, contract, manifest, receipt['media']['path'])
        bound = copy.deepcopy(receipt)
        bound.update(schema=delivery.RECEIPT_SCHEMA, render=render)
        return result, bound
    return result, None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ('receipt','export-contract','command','prepared-plan','work-dir','report'):
        parser.add_argument('--'+flag, type=Path, required=True)
    parser.add_argument('--bind-receipt', type=Path, help='New receipt path; original is never overwritten')
    parser.add_argument('--evidence', type=Path, help='Actual historical provenance assessment, required for binding')
    args = parser.parse_args()
    if bool(args.bind_receipt) != bool(args.evidence):
        parser.error('--bind-receipt and --evidence must be supplied together')
    for path in (args.report, args.bind_receipt):
        if path and path.exists():
            parser.error('Output exists: '+str(path))
    try:
        report, bound = audit(args.receipt,args.export_contract,args.command,args.prepared_plan,args.work_dir,args.evidence)
        delivery.write_json(args.report,report)
        if bound is not None:
            delivery.write_json(args.bind_receipt,bound)
        print('SETTINGS_PASS '+str(args.report))
    except (ValueError,TypeError,KeyError,OSError,IndexError,subprocess.CalledProcessError) as exc:
        delivery.write_json(args.report,{'status':'UNRESOLVED','reason':str(exc),'scope':'historical settings audit; no media changed'})
        parser.exit(2, str(exc)+'\n')


if __name__ == '__main__':
    main()
