import csv
import requests
import json

str_articlesdata_csv = 'ArticlesData.csv'
str_launchesdata_csv = 'LaunchesData.csv'
str_eventsdata_csv = 'EventsData.csv'


def write_row_launches(csvWriter, article_my_id, article_api_id, data):
    for d in data:
        csvWriter.writerow(
            [article_my_id, article_api_id, d["id"], d["provider"]])


def write_row_events(csvWriter, article_my_id, article_api_id, data):
    for d in data:
        csvWriter.writerow(
            [article_my_id, article_api_id, d["id"], d["provider"]])


# Write data to a CSV file
def writerSample(python_data):

    with open(str_articlesdata_csv, mode="w", encoding='utf-8', newline='') as csvfile1, open(str_launchesdata_csv, mode="w", encoding='utf-8', newline='') as csvfile2, open(str_eventsdata_csv, mode="w", encoding='utf-8', newline='') as csvfile3:
        # create a csv writers
        csvWriter = csv.writer(csvfile1)
        csvWriterLaunches = csv.writer(csvfile2)
        csvWriterEvents = csv.writer(csvfile3)

        # write the header
        csvWriter.writerow(["my_id", "api_id", "title", "url", "imageUrl", "newsSite",
                           "summary", "updatedAt", "publishedAt", "featured", "launches", "events"])
        csvWriterLaunches.writerow(
            ["article_my_id", "article_api_id", "launche_id", "provider"])
        csvWriterEvents.writerow(
            ["article_my_id", "article_api_id", "event_id", "provider"])

        # write  rows
        my_id = 0
        for data in python_data:

            if data['launches'] != []:
                write_row_launches(csvWriterLaunches, my_id,
                                   data["id"], data['launches'])
                data['launches'] = f"NOT_EMPTY"
            if data['events'] != []:
                write_row_events(csvWriterEvents, my_id,
                                 data["id"], data['events'])
                data['events'] = f"NOT_EMPTY"

            csvWriter.writerow([my_id, data["id"], data["title"], data["url"], data["imageUrl"], data["newsSite"],
                               data["summary"], data["updatedAt"], data["publishedAt"], data["featured"], data["launches"], data["events"]])
            my_id += 1
            if my_id >= 9_999: # hobby dev plan: 10_000
                break


def get_len(url):
    response = requests.get(url=url)
    return int(response.content, 10)


def get_data(url):
    response = requests.get(url=url)
    if response.status_code in range(200, 300):
        r = json.loads(response.content)
        return r


def main():
    total_articles = list()
    url = 'https://api.spaceflightnewsapi.net/v3'
    # count_total_articles = get_len(url + 'articles/count')
    rote = '/articles'
    param_limit = 10
    param_start = 0  # 12_003
    data = True
    print(
        f"Retrieving Spaceflight News API '{rote}' data ... _limit {param_limit} _start {param_start}")
    while(data):
        url_limit = f'{rote}?_limit={param_limit}'
        url_start = f'&_start={param_start}'
        data = get_data(url + url_limit + url_start)
        if data:
            for info in data:
                print('.', end=" ")
                total_articles.append(info)

        param_start += param_limit
    print("Creating csv files...")
    writerSample(total_articles)
    print("Done!")


if __name__ == '__main__':
    main()
