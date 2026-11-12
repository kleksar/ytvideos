# How Your TV Knows What You Watch

**Status: superseded draft (version 1).** A new Russian version 2 opens on the DVD clue and closes by returning to the disc. This English text and the existing visual score do not follow that revised story. Do not use this text for narration; revise it after the story has been discussed.

**Status:** Draft English adaptation for Paper Detour, based on the Russian discussion script. Running time is an estimate: approximately 8–10 minutes, depending on delivery. Section headings are for production and are not spoken. The English adaptation has received an independent factual review; no narration has been generated.

## Opening

In 2017, an American TV manufacturer agreed to pay two point two million dollars. The reason? What its televisions had been doing in their owners' living rooms.

This wasn't a story about a hacker breaking into a camera. Or someone accidentally leaving a microphone on.

According to a U.S. regulator, millions of these TVs were collecting information about what people watched. The FTC said viewers weren't clearly told that the feature collected viewing data.

And it happened even when a movie wasn't playing through an app on the television itself. So how could the TV know what was on the screen?

## The television in your living room

At the center of this story is a company called Vizio. In 2014, it began selling TVs that could automatically track viewing. On some older sets already in people's homes, the company installed the software remotely through an update.

Imagine buying a TV. You choose a screen, put it in your living room, and connect it to the internet. You expect to open an app, watch a movie, or turn on the news. You might even expect a few recommendations.

But according to the Federal Trade Commission, Vizio didn't clearly explain what was happening or obtain proper consent to collect viewing data.

The setting was called Smart Interactivity. Its description referred to offers and recommendations. The regulator argued that those words didn't tell buyers their TVs were collecting detailed viewing histories and sharing information with others.

The complaint alleged that data was collected from more than ten million TVs. A device people bought to watch programs had become part of a system for measuring its audience.

## How the TV recognized the picture

But how did the TV know what was playing? A movie didn't have to come from the manufacturer's own app.

The answer was in the image itself. According to the FTC, the Vizio sets sampled pixels from the screen every second and sent information about them to the company's servers. There, the samples were compared with a database of shows, movies, and ads.

Think of a music app that recognizes a song from a short clip. The idea is similar: a system uses recognizable features of the content to work out what's playing. To the viewer, it's just a picture. To the recognition system, it's something that can be matched against a library.

And there's an important distinction here. The FTC wasn't describing a camera filming the room. Nor did its account mean the television necessarily sent a full video recording. In the Vizio case, the commission described samples of pixels from the screen.

That meant the picture could come from any of the sources the regulator listed: over-the-air broadcasts, cable, a DVD player, or an external streaming device. The television still displayed the picture.

A viewer could switch apps or connect an external player. But in the system described by the FTC, the screen remained a place where the content could be recognized.

## Where the data went

Why would anyone want to know what was playing on a particular screen?

According to the FTC, Vizio shared viewing histories and IP addresses with other companies. Those companies could match an address to a household and add other information, such as an estimated age range or household size.

There was an important restriction in the agreements: the companies weren't allowed to re-identify people or households by name. But names weren't the only way to make the information useful for advertising.

If a company can connect viewing information to a household, it can use that data to measure audiences and target advertising on other devices. The television becomes more than a screen. It becomes another source of information for an advertising system.

That doesn't mean every ad on your phone came from your TV. And seeing an ad for a familiar product doesn't, by itself, prove you've been tracked. The point is narrower: the FTC described a specific way viewing information could be connected to advertising beyond the television itself.

## What happened to Vizio

In 2017, Vizio agreed to pay two point two million dollars to settle the case with the FTC and the state of New Jersey.

Money was only part of the agreement. The company also had to explain its data collection more clearly, obtain consent before collecting and sharing viewing information, and delete viewing data collected before March first, 2016, subject to exceptions in the agreement.

This was a particular case about a particular company's practices. It doesn't automatically tell us what every TV or every manufacturer does. But the method of recognizing content didn't disappear with the case.

## The 2024 study

In 2024, researchers decided to investigate another part of the story. Instead of looking into a living room, they looked at how TVs communicated over a network.

They studied automatic content recognition, or ACR, on two platforms — Samsung and LG — under U.S. and U.K. conditions. They observed network traffic associated with the feature across different viewing scenarios. The traffic was encrypted, so they analyzed connection patterns rather than inspecting its contents.

One result brings us back to external devices. In their experiment, traffic associated with content recognition appeared even when the television was used as an external display over HDMI.

The researchers also turned off several advertising and tracking settings at the same time. On the devices they tested, they then stopped observing connections to the identified content-recognition servers.

But the study can't tell us what every television in every home is doing. And it doesn't prove that switching off one feature stops all data collection. Its finding is more specific: on the tested devices, traffic to servers associated with content recognition appeared with an HDMI source too. After several settings were turned off, the researchers no longer observed that ACR traffic.

## The exposed server

In 2026, researchers at Northeastern University looked further. They studied twelve televisions running eight operating systems and found a problem in one particular content-recognition system associated with the VIDAA platform.

A server carrying recognition results allowed connections without authentication. The researchers report that in roughly three hours, they received more than 57 million recognition-result records associated with over one million TVs. That's a count of records, not people. The content categories included topics such as religion and health. Those labels described categories of content; they weren't statements about any individual viewer's beliefs or health.

After the researchers reported the vulnerability, access without authentication was closed. But when the authors checked again, they found that transmissions to the server still weren't encrypted.

This was an investigation of a specific system, not proof that every television sends data in the same way. And content recognition isn't limited to pictures. Some systems analyze the audio signal from the content itself. That doesn't mean a TV is necessarily listening to conversations in the room.

## Closing

So what can a TV owner do?

You can open the privacy settings and look for options related to viewing data, content recognition, personalized advertising, or data sharing. The names and locations depend on the model and the country, so check the manufacturer's instructions to see what each setting actually controls.

It's not a magic invisibility button. But it can reveal a choice you might not have known you had.

Vizio's story began with a television in an ordinary living room and ended with a two point two million dollar settlement. And in between was an unexpected discovery: to find out what a viewer was watching, the device didn't need to watch the viewer.

It watched the screen.

## Sources for production

- FTC, Vizio case overview: https://www.ftc.gov/business-guidance/blog/2017/02/what-vizio-was-doing-behind-tv-screen
- FTC complaint: https://search.ftc.gov/system/files/documents/cases/170206_vizio_2017.02.06_complaint.pdf
- FTC settlement order: https://www.ftc.gov/system/files/documents/cases/170206_vizio_stipulated_proposed_order.pdf
- 2024 IMC study: https://arxiv.org/abs/2409.06203
- Northeastern researchers, “Watching the Watchers”: https://watchingthewatchers.github.io/watchingthewatchers/paper.pdf
