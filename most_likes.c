#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <oauth.h>
#include <json-c/json.h>

#define CONSUMER_KEY "your_consumer_key"
#define CONSUMER_SECRET "your_consumer_secret"
#define ACCESS_TOKEN "your_access_token"
#define ACCESS_TOKEN_SECRET "your_access_token_secret"

size_t write_data(void *ptr, size_t size, size_t nmemb, struct string *s)
{
    size_t new_len = s->len + size*nmemb;
    s->ptr = realloc(s->ptr, new_len+1);
    if (s->ptr == NULL) {
        fprintf(stderr, "realloc() failed\n");
        exit(EXIT_FAILURE);
    }
    memcpy(s->ptr+s->len, ptr, size*nmemb);
    s->ptr[new_len] = '\0';
    s->len = new_len;

    return size*nmemb;
}

struct string {
    char *ptr;
    size_t len;
};

char *url_encode(const char *str)
{
    CURL *curl = curl_easy_init();
    char *output = curl_easy_escape(curl, str, 0);
    curl_easy_cleanup(curl);
    return output;
}

char *get_user_timeline(const char *user_handle)
{
    struct string s;
    s.ptr = malloc(1);
    s.len = 0;

    char *user_handle_encoded = url_encode(user_handle);
    char url[256];
    snprintf(url, sizeof(url), "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=200", user_handle_encoded);

    oauth_consumer_key = CONSUMER_KEY;
    oauth_consumer_secret = CONSUMER_SECRET;
    oauth_token = ACCESS_TOKEN;
    oauth_token_secret = ACCESS_TOKEN_SECRET;

    oauth_signature_method_hmac_sha1(data, url, &oauth_consumer_key, &oauth_consumer_secret, &oauth_token, &oauth_token_secret);
    curl_global_init(CURL_GLOBAL_DEFAULT);

    CURL *curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, NULL);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &s);

        CURLcode res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
            exit(EXIT_FAILURE);
        }

        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();

    free(user_handle_encoded);

    return s.ptr;
}

void get_most_liked_tweet(const char *user_handle)
{
    char *timeline = get_user_timeline(user_handle);

    struct json_object *json = json_tokener_parse(timeline);
    if (json == NULL) {
        fprintf(stderr, "Failed to parse JSON response\n");
        exit(EXIT_FAILURE);
    }

    struct json_object *tweet_array;
    json_object_object_get_ex(json, "tweet_array", &tweet_array);

    struct json_object *most_liked_tweet = NULL;
    int max_likes = 0;

    int num_tweets = json_object_array_length(tweet_array);
    for (int i = 0; i < num_tweets; i++) {
        struct json_object *tweet = json_object_array_get_idx(tweet_array, i);

        struct json_object *favorite_count;
        json_object_object_get_ex(tweet, "favorite_count", &favorite_count);
        int likes = json_object_get_int(favorite_count);

        if (likes > max_likes) {
            most_liked_tweet = tweet;
            max_likes = likes;
        }
    }

    if (most_liked_tweet != NULL) {
        struct json_object *tweet_id;
        json_object_object_get_ex(most_liked_tweet, "id_str", &tweet_id);
        const char *tweet_text = json_object_get_string(tweet_id);

        struct json_object *tweet_text;
        json_object_object_get_ex(most_liked_tweet, "text", &tweet_text);
        const char *tweet_text = json_object_get_string(tweet_text);

        printf("Most Liked Tweet:\n");
        printf("Tweet ID: %s\n", tweet_id);
        printf("Text: %s\n", tweet_text);
        printf("Likes: %d\n", max_likes);
    } else {
        printf("No tweets found for user: %s\n", user_handle);
    }

    free(timeline);
}

int main()
{
    char user_handle[100];
    printf("Enter the Twitter handle of the user: ");
    fgets(user_handle, sizeof(user_handle), stdin);
    user_handle[strcspn(user_handle, "\n")] = 0;

    get_most_liked_tweet(user_handle);

    return 0;
}
