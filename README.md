# OpenClassrooms Course Downloader

###### 



## What does it do ?

It allows you to download the course pages and videos so that you can **learn offline** / on the go. (or have a versioned history of it in case the course might receive substantial changes in the future).

On top of that, it allows you to bypass the maximum number of videos you can view each week, by downloading them instead.



**Features**:

- course pages as markdown (you can use [Typora](http://typora.io/) to read them)
- course pages as HTML
- Course videos : you choose the video quality among those available (typical courses have these video definitions *360p*, *540p*, *720p*, *1080p*).



## Installing

You will need to have the following dependencies installed:

- `Selenium`  (installation instructions can be found [here](https://selenium-python.readthedocs.io/installation.html))



**Python dependencies**

You can install python dependencies with one command: `pip install requests bs4 lxml tomd requests_download progressbar`.

Otherwise, you can do it one by one.

- `requests` : install with `pip install requests`
- `BeautifulSoup` and `lxml` : install with `pip install bs4 lxml`
- `tomd` for transforming HTML to Markdown files. (`pip install tomd`)
  You can also use another Markdown converter by tampering with the `markdown.py` file.



**Optional Python dependencies**

- `requests_download` and `progressbar` in order to have a neat progress bar when downloading the course's video files. If not, a message will simply be written in the command line when the download starts.





**Getting the code from the repo**

```bash
git clone https://github.com/JeffMv/OCCourseDownloader.git
cd OCCourseDownloader

# use it
python oc_course_downloader_selenium.py --help
```





## Usage



```bash
python ./oc_course_downloader_selenium.py -d <destination_folder> --username <username> course_url [course_url ...]


# Example command to download the course "Testez votre projet avec Python"
python oc_course_downloader_selenium.py -d "/volumes/my-usb-key/Downloads" -u myusername "https://openclassrooms.com/fr/courses/4425126-testez-votre-projet-avec-python/"

# Not specifying the -p argument will prompt you to enter your password securely without showing it in the console.

```





## More Features ?

Maybe some people might be interested by some new features. PR if you want these or more features:

- replacing `<img>` and `<iframe>` tags' references with the actual downloaded files.
  With video iframes, it would mean replacing them with `<video>` tags.



## Enjoy

After you have successfully downloaded a course, you might want to browse the course either as HTML or as Markdown.

**Markdown editors**

-  [Typora](http://typora.io) : At the time of writting, it is still *free* in beta version, so you might just hop on the occasion.



If you found this script useful, drop a star or a comment ;)

