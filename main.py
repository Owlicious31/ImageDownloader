import os
import requests
from bs4 import BeautifulSoup

PARSER = "html.parser"
GOOGLE_SEARCH_URL = "https://www.google.com/search?udm=2&q=[query]"


def download_directory_exists(download_dir: str | None) -> bool:
    """
    Check if the provided directory exests if not create a 'downloads' directory in the current directory.
    If no download directory is provided a directory will be made in the current directory.

    :param download_dir: The directory downloads will be saved to.
    :return: bool
    """
    if not download_dir:
        if not os.path.exists("./downloads"):
            os.mkdir("./downloads")
        return False

    elif not os.path.exists(download_dir):
        if not os.path.exists("./downloads"):
            os.mkdir("./downloads")
        return False
    
    else:
        return True


def fetch_images(search_choice: str,num_images: int,download_location: str | None = None) -> None:
    """
    Fetch top images on Google search using the BeautifulSoup webscraper.
    Only able to fetch 20 images currently.

    :param search_choice: The search query to be sent to Google Search.
    :param num_images: The number of images to download. Max 20.
    :param download_location: The location the acquired image files will be saved to.
    :return: None
    """
    if download_directory_exists(download_dir=download_location):
        download_dir = download_location
    
    else:
        download_dir = "./downloads"

    if num_images > 20:
        print("The number of images should be twenty or less.")
        return

    search_url = GOOGLE_SEARCH_URL.replace("[query]",search_choice)

    contents = requests.get(url=search_url).content
    soup = BeautifulSoup(markup=contents,features=PARSER)
    
    images = soup.select(selector=".kCmkOe img",limit=num_images)
    image_contents = [image.get(key="src") for image in images if image.get(key="src")]
    image_contents = [requests.get(image_content).content for image_content in image_contents] 

    for i,image in enumerate(image_contents):
        with open(f"{download_dir}/{search_choice}-{i + 1}.png",mode="wb") as file:
            file.write(image)


def main() -> None:
    search_choice = input("What images would you like to download? ")
    num_images = int(input("How many of these images would you like? "))
    download_location = input("Where do you want to your images to be saved?[enter nothing to use the default location] ")

    fetch_images(search_choice=search_choice,num_images=num_images,download_location=download_location)

if __name__ == "__main__":
    main()
