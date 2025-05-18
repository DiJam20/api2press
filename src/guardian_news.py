import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, NavigableString

load_dotenv()

def fetch_guardian_news(section_filter, hours_back):
    """
    Fetch raw articles from The Guardian API

    :param section_filter: pipe-seperated string of section IDs
    :param hours_back: maximum age (in hours) that an article may have to be considered
    :return: dictionary with API response containing all articles
    """
    url = 'https://content.guardianapis.com/search'

    # Calculate date 12 hours back
    fresh_news_date = (datetime.now() - timedelta(hours=hours_back)).strftime('%Y-%m-%d')

    # Parameters for TheGuardian API request
    params = {
        'api-key': os.getenv('GUARDIAN_API_KEY'),
        'section': section_filter,                  # Filter articles from world news, opinion, and lifestyle
        'page-size': 200,          # Number of articles fetched (max 200)
        'show-fields': 'headline,trailText,byline,body,thumbnail,wordcount',
        'order-by': 'relevance',                    # Order results dict by the relevance assigned by editors
        'from-date': fresh_news_date,               # From past 12 hours
    }

    # Get JSON response from API
    response = requests.get(url, params=params)
    response.encoding = 'utf-8' # The Guardian API sends UTF-8 encoded data
    response.raise_for_status()
    # Parse the JSON response into a Python dictionary
    api_response = response.json()

    return api_response


def clean_article_html(html_content):
    """
    Strip links from text and remove all figures.

    :param html_content: text of the body of one article
    :return: clean body text of one article
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove links
    for a_tag in soup.find_all('a'):
        a_tag.replace_with(NavigableString(a_tag.text))  # Text without link

    # Remove figures
    for figure in soup.find_all('figure'):
        figure.decompose()  # Remove figures

    return str(soup)


def process_articles(api_response):
    """
    Store all relevant details of the API response in a dictionary.
    :param api_response: dictionary containing all details of API response
    :return: list of dictionaries each containing the relevant metadata of one article
    """
    unfiltered_news_items = []

    for news_item in api_response['response']['results']:
        try:
            section_id = news_item.get('sectionId', '')
            section_name = news_item.get('sectionName', '')
            date_published = news_item.get('webPublicationDate', '')
            title = news_item.get('webTitle', '')
            subheading = news_item.get('fields', {}).get('trailText', '')
            author = news_item.get('fields', {}).get('byline', '')
            main_text = news_item.get('fields', {}).get('body', '')
            thumbnail = news_item.get('fields', {}).get('thumbnail', '')
            wordcount = news_item.get('fields', {}).get('wordcount', '')

            main_text = clean_article_html(main_text)

            unfiltered_news_items.append({
                'section_id': section_id,
                'section_name': section_name,
                'date_published': date_published,
                'title': title,
                'subheading': subheading,
                'author': author,
                'main_text': main_text,
                'thumbnail': thumbnail,
                'wordcount': wordcount
            })
        except Exception as e:
            print(f'Error processing article: {news_item.get('webTitle', 'Unknown')}, {str(e)}')
            continue

    # Remove all live feeds ('as it happened') stories
    news_items = [story for story in unfiltered_news_items if 'as it happened' not in story['title']]

    return news_items


def select_section_highlights(news_items, section_filter):
    """
    First, remove any live feed articles.
    Second, find the first article that matches each specified section. The articles are ordered by relevance, so
    this will find the most important article of each section.
    :param news_items: list of dictionaries each containing the relevant metadata of one article
    :param section_filter: pipe-seperated string of section IDs
    :return: list of dictionaries for each top article, one from each section
    """

    # Find the top article for each of the section specified in the filter
    top_articles = []
    sections = section_filter.split('|')

    for section in sections:
        section_article = next(story for story in news_items if story['section_id'] == section)
        top_articles.append(section_article)

    return top_articles


def get_guardian_news(section_filter, hours_back):
    """
    Use The Guardian API to fetch all news in the specified 'section_filter' sections
    and in the past 'hours_back' hours. Returns a JSON object.
    Process the JSON object, keeping only relevant information and removing HTML artefacts.
    Then select the top articles of the specified sections.

    :param section_filter: pipe-seperated string of section IDs
    :param hours_back: maximum age (in hours) that an article may have to be considered
    :return: processed list containing the top article of each specified section
    """
    api_response = fetch_guardian_news(section_filter, hours_back)
    all_the_articles = process_articles(api_response)
    articles = select_section_highlights(all_the_articles, section_filter)

    return articles