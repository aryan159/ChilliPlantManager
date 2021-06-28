# ChilliPlantManager
A program to count the number of red chillies on a chilli plant

# Thought process

<img src="https://user-images.githubusercontent.com/33245117/109410579-be717180-79d6-11eb-8212-32cb6c1629af.jpeg" width="400" height="533">
This is the chilli plant that my brother recently brought home. He would monitor it everyday, count the number of red chillies and green chillies and see if any of them are ripe enough for picking. I knew that, like all 14 year olds, he was eventually going to lose interest so I decided to see if I could create a program to do it.

# Initial plan

Have a microcontroller with a camera module take photos of the plant everyday at a fixed time and send it to my program. Then, analyse the photo, counting the number of red chillies, green chillies and flowers and display the information on a website or a telegram chat. This initial plan is ,admittedly, very abmitious but I am using it to explore the different domanins of software development, namely, networking, computer vision, data structures and algorithms and front-end development. To start this project, I decided to start on the part that I believe is the toughest to see if I could actually realise my end goal.

# Counting the Chillies

![image](https://user-images.githubusercontent.com/33245117/109419800-2ee5b600-7a0a-11eb-936a-fca916665f20.png)
![image](https://user-images.githubusercontent.com/33245117/109419772-12e21480-7a0a-11eb-87a0-b67e49051885.png)


# Learnings

![image](https://user-images.githubusercontent.com/33245117/109413756-14034980-79ea-11eb-9dad-334917e54911.png)

I decided to really think about readibility in this project and came to the realisation that redundancy, if done correctly, can do great things for readibility without any drawbacks. I imagined myself coming back to this project a few months or even years later and realised that by using the explicit tuple() constructor, it is immediately obvious what I am doing. This is especially true if the reader has not used python for a while and cannot immediately realise that adding the extra round brackets implies the creation of a tuple