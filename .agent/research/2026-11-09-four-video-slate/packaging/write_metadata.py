from pathlib import Path
r=Path('/Users/diplomat/ytvideos')
eps={
'cable':r/'channels/paper_detour/research/2026-11-09-atlantic-cable/Packaging/Metadata',
'us':r/'channels/nuviko_history/research/us-history/Packaging/Metadata',
'neptune':r/'channels/paper_detour/research/2026-11-09-neptune/Packaging/Metadata',
'harrison':r/'channels/nuviko_history/research/harrison-packaging/Metadata'}
data={
'cable':[
('The First Atlantic Cable Worked. Then It Went Silent.','In 1858, a message crossed the Atlantic by telegraph for the first time. Within weeks, the cable fell silent.\n\nFrom the first attempts at sea to the recovery of a lost cable in 1866, follow the people and inventions that made a lasting connection possible.'),
('The Lost Cable That Was Recovered From the Ocean Floor','The Great Eastern was hundreds of miles from Newfoundland when its telegraph cable snapped and disappeared into the Atlantic.\n\nA year later, the ship returned to search the seabed. This is the story of the long struggle to connect two continents—and the cable the crew brought back from the deep.'),
('The Tiny Mirror That Helped Connect Two Continents','A signal sent across the Atlantic could emerge too weak and blurred to read. One solution used a tiny mirror and a beam of light.\n\nDiscover how the mirror receiver worked, why the first cable failed, and how the Great Eastern finally helped establish a durable transatlantic telegraph connection.')],
'us':[
('America Tried to Buy a City. France Offered Much More.','In 1803, American negotiators wanted New Orleans, a port vital to trade on the Mississippi. France offered them the vast territory of Louisiana.\n\nThe purchase transformed the scale of the United States. As the country expanded, conflict over slavery, political power and Indigenous land intensified until the Union faced civil war.'),
("How America's Expansion Fueled a Fight Over Slavery",'As the United States expanded west, every new territory raised a question: would slavery be allowed there?\n\nFrom the Louisiana Purchase and the Missouri Compromise to Kansas, the Supreme Court and civil war, follow the struggle over land, power and freedom that reshaped the country.'),
("The Fight Over America's Future That Led to Civil War",'The United States grew across a continent, but each new state reopened a struggle over slavery and political power.\n\nThis history follows the Louisiana Purchase, forced Cherokee removal, expansion and the crisis that split the Union—then traces the war and abolition that followed.')],
'neptune':[('The Planet Found With Math #Neptune #SpaceHistory','Uranus was not quite where astronomers expected it to be. Could another planet be pulling it off course?\n\nIn 1846, Urbain Le Verrier calculated where to look. At the Berlin Observatory, Johann Galle and Heinrich d’Arrest compared the sky with a star chart—and found a point of light missing from the chart. The next night it had moved: Neptune had been found.')],
'harrison':[('How a Clock Helped Sailors Find Their Way #JohnHarrison #Longitude','How could a clock help a ship find its position in the middle of the ocean? Sailors could compare local noon with the time back home to work out how far east or west they had travelled—but only if their clock stayed accurate at sea.\n\nEnglish clockmaker John Harrison spent years tackling the problem. In 1761, his son took Harrison’s H4 timekeeper on a voyage to Jamaica, putting the watch to the test.')]}
tags={'cable':'#History #TransatlanticCable #Telegraph #TechnologyHistory #MaritimeHistory','us':'#AmericanHistory #LouisianaPurchase #CivilWar #USHistory #History','neptune':'#Neptune #Astronomy #SpaceHistory #History #Shorts','harrison':'#History #JohnHarrison #Longitude #MarineChronometer #MaritimeHistory #Navigation #Clockmaking #Sailing #Shorts'}
music={'cable':'Music: “Signal to Noise — No Piano Melody” by Scott Buckley, CC BY 4.0: https://www.scottbuckley.com.au/library/signal-to-noise/','us':'Music: “Signal to Noise — No Piano Melody” by Scott Buckley, CC BY 4.0: https://www.scottbuckley.com.au/library/signal-to-noise/ ; “Night Vigil” by Kevin MacLeod, CC BY 4.0: https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1900047','neptune':'Music: “Signal to Noise — No Piano Melody” by Scott Buckley, CC BY 4.0: https://www.scottbuckley.com.au/library/signal-to-noise/','harrison':'Music: “Thinking Music” by Kevin MacLeod, shortened, faded and mixed with narration, CC BY 4.0: https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1600060 .\n\nVisual reference for H4: “H4 timekeeper” by Jordiferrer, adapted into generated scenes; CC BY-SA 4.0: https://commons.wikimedia.org/wiki/File:H4_timekeeper.jpg .'}
for key,items in data.items():
 p=eps[key]; p.mkdir(parents=True,exist_ok=True)
 chapters=(p/'chapters.txt').read_text().strip() if key in ('cable','us') else ''
 for i,(title,body) in enumerate(items):
  suffix=chr(65+i)
  (p/f'title-{suffix}.txt').write_text(title+'\n')
  (p/f'description-{suffix}.txt').write_text(body+'\n\n'+(chapters+'\n\n' if chapters else '')+music[key]+'\n\n'+tags[key]+'\n')
print('8 full titles and descriptions written')
