# OC Course Downloader



## What does it do ?

It allows you to download the course pages and videos so that you can **learn offline** / on the go. (or have a versioned history of it in case the course might receive substantial changes in the future).

On top of that, it allows you to bypass the maximum number of videos you can view each week, by downloading them instead.



**Features**:

- course pages as markdown (you can use [Typora](http://typora.io/) to read them)
- course pages as HTML
- Course videos : you choose the video quality among those available (typical courses have these video definitions *360p*, *540p*, *720p*, *1080p*).



## Installing

You will need to have the following dependencies installed:

- `BeautifulSoup` and `lxml`
- `Selenium` 
- `tomd` for transforming HTML into Markdown.
  You can also use another Markdown converter by tampering with the `markdown.py` file.




## Usage



```bash
python ./oc_course_downloader_selenium.py --courseUrls course_url [course_url ...] -d <destination_folder> --username <username>


# Example command to download the course "Testez votre projet avec Python"
python oc_course_downloader_selenium.py --courseUrls "https://openclassrooms.com/fr/courses/4425126-testez-votre-projet-avec-python/4435224-utilisez-des-mocks" -d "/volumes/my-usb-key/Downloads" -u myusername
# this will prompt you to enter your password without showing it in the console.




## Enjoy

After you have successfully downloaded a course, you might want to browse the course either as HTML or as Markdown.

I'd personnally recommend [Typora](http://typora.io) as a Markdown editor/reader <3. At the time of writting, it is still *free* in beta version, so you might just hop on the occasion.



If you found this script useful, drop a star or a comment ;)