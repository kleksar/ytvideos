from pathlib import Path
import json,hashlib
EP=Path(__file__).resolve().parents[3];OUT=EP/'Edit/Production/v02'
rows='''01|0|5.60|host|How Do You Fix Voyager 1 From 24 Billion Kilometers Away?|Traveler in separate explanatory space with Earth and a distant Voyager visualization.
02|5.60|10.50|space|In 1977, humanity sent a spacecraft called Voyager 1|Wide view of Voyager leaving a small Earth behind.
03|10.50|15.30|space|to Jupiter and Saturn. After completing its mission|Voyager against a large Jupiter, showing small spacecraft scale.
04|15.30|20.17|space|it kept traveling, becoming the most distant operating spacecraft|Saturn recedes behind Voyager; open dark space ahead.
05|20.17|24.37|space|Decades later, in November 2023|Voyager isolated, fragmented conceptual data marks near its antenna; not actual telemetry.
06|24.37|28.87|reconstruction|its messages stopped making sense back on Earth.|Anonymous engineer over shoulder at unreadable abstract monitor; reuse original05.
07|28.87|33.37|diagram|The spacecraft was still receiving commands.|Earth left and Voyager right, clear Earth-to-spacecraft command line.
08|33.37|37.70|diagram|But neither its scientific measurements nor the information about its own condition|Science and status channels reach Earth as unreadable abstract data; radio link persists.
09|37.70|43.30|host|How do you figure out what's broken|Thoughtful guide facing a sealed conceptual state block, separate from history.
10|43.30|47.90|space|By then, Voyager 1 was about 24 billion kilometers from Earth.|Extremely wide dark space and a tiny Voyager, scale conceptual.
11|47.90|52.50|diagram|In 2012, it had crossed the boundary of the heliosphere|Sun within conceptual heliosphere; Voyager outside; no solid physical shell.
12|52.50|57.10|diagram|the enormous region around the Sun shaped by the solar wind and magnetic field.|Wide explanatory region, stylized solar-wind and field lines, not real geometry.
13|57.10|61.70|space|Beyond that boundary, it had begun studying interstellar space.|Spacecraft beyond receding conceptual boundary, subdued deep stars.
14|61.70|67.60|space|There was no way to reach it and replace a part.|Isolated Voyager in vast dark space, no physical access or visitors.
15|67.60|72.80|diagram|But even that required patience. A command sent from Earth|Long outgoing Earth-to-Voyager route, 22.5-hour conceptual delay.
16|72.80|78.00|diagram|The reply took just as long to return.|Same endpoint positions, return route toward Earth and equal delay.
17|78.00|83.20|reconstruction|To find out whether a single attempt had worked|Anonymous engineer waits at plain monitor; reuse original19.
18|83.20|87.20|reconstruction|They spent months searching for the cause.|Two anonymous engineers discuss problem; reuse original20.
19|87.20|91.20|diagram|Their suspicions turned to one of the onboard computers.|Voyager with a separate abstract computer block; no physical internal equipment layout.
20|91.20|95.20|diagram|It collected scientific and engineering data|Science and engineering inputs converge at computer block and enter transmission route.
21|95.20|99.93|diagram|In March 2024, the team sent a diagnostic command.|Earth left sends one diagnostic command to Voyager right.
22|99.93|104.63|reconstruction|Once again, unusual data came back. But this time|Engineer examines abstract information becoming structured, no victory reaction.
23|104.63|109.37|diagram|It was the contents of the onboard computer's memory.|Close conceptual memory-information grid, no code or addresses.
24|109.37|115.27|diagram|By comparing it with earlier records, they found the problem.|Earlier and current memory-information diagrams compared; damage appears only in current.
25|115.27|121.17|diagram|About three percent of the memory had been damaged.|Conceptual 3 percent damage and overlap with message-preparation instructions.
26|121.17|126.20|diagram|They couldn't repair the chip onboard.|Same damage remains unavailable; nothing is physically replaced or repaired.
27|126.20|131.20|diagram|But they could try moving the necessary instructions into undamaged memory.|Program instructions adjacent to separated undamaged spaces; proposed relocation.
28|131.20|135.20|host|No single free section of memory was large enough|Guide measures separated empty spaces; entire program fragment is too long.
29|135.20|140.50|diagram|So the engineers split the code into smaller pieces|One logical program split and placed into separate intact areas; fragment count schematic only.
30|140.50|145.80|diagram|Then they had to change the references inside the program|Abstract links redirect to new instruction locations; damaged area remains untouched.
31|145.80|151.13|diagram|so the computer could find the instructions at their new addresses|Linked relocated parts form one working sequence around the unavailable area.
32|151.13|155.17|diagram|They decided to start with the program that prepared information|Spacecraft-status processing selected first; science branch still inactive.
33|155.17|159.20|reconstruction|If they could restore even that|Engineer studies still-unrecovered status; conditional expectation, no success signal.
34|159.20|163.27|diagram|the team would once again be able to see how its systems were working.|Dashed proposed spacecraft-status path to Earth; target, not received result.
35|163.27|168.00|reconstruction|On April 18, they sent the fix from Earth.|Keyboard/hands sending fix; reuse original41 for April18.
36|168.00|173.67|diagram|It took almost a full day to reach Voyager.|Two opposite routes as sequential parts of same exchange; outbound then return.
37|173.67|177.97|reconstruction|On April 20, engineers received a message they could actually read.|Engineer reads coherent conceptual blocks; reuse original44 for April20.
38|177.97|182.27|diagram|For the first time in five months|Unreadable old information compared with newly ordered spacecraft-status blocks.
39|182.27|186.57|diagram|the spacecraft had sent back understandable information about the condition of its systems.|Ordered spacecraft-status information returns to Earth; science remains separate.
40|186.57|191.77|reconstruction|Now they could turn to the scientific measurements.|Two anonymous engineers turn to conceptual science information, no actual measurements.
41|191.77|196.97|diagram|By June, data was once again arriving from all four instruments|Four conceptual science sources merge into one Earth-bound link, June2024.
42|196.97|201.90|diagram|The damaged memory remained damaged.|Original damaged region stays dark, no recovery of the damaged cells.
43|201.90|206.83|diagram|But the engineers had found a way around it.|Working program route uses intact memory and bypasses same damaged area.
44|206.83|211.7667|space|And a spacecraft launched almost half a century earlier|Extreme wide deep-space Voyager, coherent silhouette, quiet continued research.'''
scenes=[]
for line in rows.splitlines():
 sid,start,end,typ,anchor,meaning=line.split('|');sf=round(float(start)*30);ef=round(float(end)*30);assert 120<=ef-sf<=180
 scenes.append({'id':f'S{sid}','start_frame':sf,'end_frame':ef,'type':typ,'narration_anchor':anchor,'composition':meaning,'depiction':'conceptual explanation' if typ in ('diagram','space','host') else 'anonymous historical reconstruction'})
assert scenes[0]['start_frame']==0 and scenes[-1]['end_frame']==6353 and all(a['end_frame']==b['start_frame'] for a,b in zip(scenes,scenes[1:]))
(OUT/'shotmap_v02.json').write_text(json.dumps({'version':'v02','fps':30,'frame_count':6353,'consultation':'https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6aeb532f-0e20-83eb-979c-9dc810402337','source_note':'Coordinator complete table transfer from personally read Extra High response, with English composition descriptions. Time anchors are semantic, not verified word onsets.','coordinator_adaptations':['Computer block remains separate from Voyager, avoiding invented internal layout.','Percentage diagram is conceptual, not an assertion of cell geometry or actual addresses.'],'scenes':scenes},ensure_ascii=False,indent=2)+'\n')
print(len(scenes),'scenes; all 4–6s; frames',scenes[-1]['end_frame'])
