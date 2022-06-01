# CambossChecks

## Campering Tampering Detection:
Tampering Detecion is a process of detecting the kind of anomalies in the video. These anomalies can be defined as per our objectives and create a model to detect the 
tampering.

Tampering Detection over here is when there is a significant changes in the camera orientation angle or direction then it is to be detected and considered tampering 
detection strictly.

Video is a series of frame's and making comparison to each frame till the end of frames in a video helps us to tampering detection.

For this, a baseline image is taken initially for the comparison and defined as required background where camera needs to be pointed always to it. 

firstly, Substract the foreground images slightly with some threshold in ordrer to not influence the tampering detection due to foreground objects and then apply the 
required opencv transformations and techniques in order to compare baseline frame to the rest of the frames.

When there is a change in the background of the frames with similarity value that is reducing beyond some threshold point is considered as tampering detection.

## paint spray detection:
Paint spray detection works as when paint is sprayed then the pixels of the images suddenly or gradually turns to black and then all this pixels are blacked out.

Paint spray may not turns out all the pixels to pure black but applying the edge cascades like threshold method which changes to black with some threshold value and rest 
to the white pixels with this method. so, manually enhancing the pixels intensity when there is a paint spray that is affecting all the pixels value helps us to detect
the paint spray detection.

Customization of detection: This is just because most of the times camera frame's consists of timestamps on it and those pixels will not get affected to the paint spray.

So masking is a technique kind of similar to cropping the image which will consider only requied part of the frame rather than complete frame for the paint spray 
detection

Blur detection: blur detection particularly here is defined as the low amount of high frequencies of the pixels considered as blurry. blur detection works  
when a clear image is reduced to a very highly lower resolution of it but beneficially here it is helping us when there is an occlusion of the image with opaque objects
because of all similar pixels colors or low amount of high frequencies of the image.

so, these two are detection models to detect the tampering in the series of frames.
