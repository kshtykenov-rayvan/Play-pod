# utils/tube_search.py

from youtube_search import YoutubeSearch


def search_youtube(query: str, max_results: int = 5) -> list:
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    video_list = []

    for video in results:
        info = {
            "title": video['title'],
            "link": f"https://www.youtube.com{video['url_suffix']}",
            "channel": video['channel'],
            "duration": video['duration'],
            "views": video['views'],
            "publish_time": video['publish_time']
        }
        video_list.append(info)

    return video_list


if __name__ == "__main__":
    query = input("Введите запрос: ").strip()
    results = search_youtube(query)

    if not results:
        print("Ничего не найдено.")
    else:
        for i, video in enumerate(results, 1):
            print(f"{i}. {video['title']}")
            print(f"   Ссылка: {video['link']}")
            print(f"   Канал: {video['channel']}")
            print(f"   Длительность: {video['duration']}, Просмотры: {video['views']}, Дата: {video['publish_time']}")
            print("-" * 50)