# ChilliPlantManager
A program to count the number of red chillies on a chilli plant

# Environment Setup
I used the anaconda interpreter since I was easily able to import numpy and cv2 through it

# Inspiration

<img src="https://user-images.githubusercontent.com/33245117/109410579-be717180-79d6-11eb-8212-32cb6c1629af.jpeg" width="400" height="533">
This is the chilli plant that my brother recently brought home. He would monitor it everyday, count the number of red chillies and green chillies and see if any of them are ripe enough for picking. I knew that, like all 14 year olds, he was eventually going to lose interest so I decided to see if I could create a program to do it.


# Counting the Chillies
Initially I tried to find the chillies by extracting the raw RGB data, but to no avail. I then stumbled upon an alternative to the RGB model called HSV (Hue, Saturation, Value)

<img src="https://user-images.githubusercontent.com/33245117/145162810-b5f87234-93ef-473d-bf3f-01a463a811fa.png" width="318" height="281">
Using this colour system, it was much easier to single out the red chillies.

In the first part of the code, the user slides the thresholds for desired Hue, Saturation and Value values until the red pixels are singled out

<img src="https://user-images.githubusercontent.com/33245117/123677635-f4850c00-d877-11eb-9e0e-7037577b7a42.png" width="800" height="500">

Then based on those values, the program generates a 2d array with all the red pixels marked. The red pixels are then grouped together by proximity using an algorithm that goes through the entire array, finds the red pixels, scans around the current red pixel to find more red pixels and then scans around those newly found red pixels until all red pixels have been grouped together in their own groups (chillies)

![Screenshot 2021-06-29 005820](https://user-images.githubusercontent.com/33245117/123676828-ff8b6c80-d876-11eb-8d1e-e459fc7eb458.png)
![Screenshot 2021-06-29 010022](https://user-images.githubusercontent.com/33245117/123676842-02865d00-d877-11eb-94c1-3801384d7f69.png)

The program then outputs the initial input image with white numberings showing where all the chiilies are. (You might have to look closely to see the white annotations) The program was able to find every chilli and counted the chillies correctly even when they were "cut" in half by a green branch (e.g 2nd Image, Chilli #5)

# Learnings

![image](https://user-images.githubusercontent.com/33245117/109413756-14034980-79ea-11eb-9dad-334917e54911.png)

I decided to really think about readibility in this project and came to the realisation that redundancy, if done correctly, can do great things for readibility without any drawbacks. I imagined myself coming back to this project a few months or even years later and realised that by using the explicit tuple() constructor, it is immediately obvious what I am doing. This is especially true if the reader has not used python for a while and cannot immediately realise that adding the extra round brackets implies the creation of a tuple
