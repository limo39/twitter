#include <stdio.h>
#include <curl/curl.h>
#include <oauth.h>

#define CONSUMER_KEY "YOUR_CONSUMER_KEY"
#define CONSUMER_SECRET "YOUR_CONSUMER_SECRET"
#define ACCESS_TOKEN "YOUR_ACCESS_TOKEN"
#define ACCESS_SECRET "YOUR_ACCESS_SECRET"

int main(void) {
    CURL *curl;
    struct curl_slist *headers = NULL;
    char oauth_header[1024];

    char tweet_id[20] = "TWEET_ID_TO_DELETE";

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();

    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.twitter.com/1.1/statuses/destroy.json");

        oauth_signature_method_hmac_sha1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET);
        snprintf(oauth_header, sizeof(oauth_header), "%s", oauth_header);
        headers = curl_slist_append(headers, oauth_header);

        curl_easy_setopt(curl, CURLOPT_POST, 1L);

        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, tweet_id);

        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

        CURLcode res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }

        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
    }

    curl_global_cleanup();
    return 0;
}
