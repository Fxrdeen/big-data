package main

import (
	"fmt"
	"net/http"
	"github.com/Shopify/sarama"
	"time"
)

var (
	producer sarama.AsyncProducer
)

// Initialize Kafka producer
func initProducer() sarama.AsyncProducer {
	config := sarama.NewConfig()
	config.Producer.Return.Successes = true
	config.Producer.Flush.Frequency = 500 * time.Millisecond
	producer, err := sarama.NewAsyncProducer([]string{"localhost:9092"}, config)
	if err != nil {
		panic(err)
	}
	return producer
}

// API handler for emoji submissions
func emojiHandler(w http.ResponseWriter, r *http.Request) {
	emoji := r.URL.Query().Get("emoji")
	if emoji == "" {
		http.Error(w, "Emoji not specified", http.StatusBadRequest)
		return
	}
	// Send to Kafka asynchronously
	go func() {
		producer.Input() <- &sarama.ProducerMessage{
			Topic: "emoji-stream",
			Value: sarama.StringEncoder(emoji),
		}
	}()
	fmt.Fprintln(w, "Emoji received")
}

func main() {
	producer = initProducer()
	defer producer.Close()
	http.HandleFunc("/send_emoji", emojiHandler)
	http.ListenAndServe(":8080", nil)
}

