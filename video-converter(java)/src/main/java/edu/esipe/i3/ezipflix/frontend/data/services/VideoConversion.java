package edu.esipe.i3.ezipflix.frontend.data.services;

import com.amazonaws.regions.Regions;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Item;
import com.amazonaws.services.dynamodbv2.document.PutItemOutcome;
import com.amazonaws.services.dynamodbv2.document.Table;
import com.fasterxml.jackson.core.JsonProcessingException;
import edu.esipe.i3.ezipflix.frontend.ConversionRequest;
import edu.esipe.i3.ezipflix.frontend.ConversionResponse;
import edu.esipe.i3.ezipflix.frontend.data.entities.VideoConversions;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.core.MessageProperties;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.TimeZone;
import java.util.UUID;

/**
 * Created by Gilles GIRAUD gil on 11/4/17.
 */
@Service
public class VideoConversion {

    @Value("${conversion.messaging.rabbitmq.conversion-queue}") public  String conversionQueue;
    @Value("${conversion.messaging.rabbitmq.conversion-exchange}") public  String conversionExchange;


    @Autowired RabbitTemplate rabbitTemplate;


//    @Autowired
//    @Qualifier("video-conversion-template")
//    public void setRabbitTemplate(final RabbitTemplate template) {
//        this.rabbitTemplate = template;
//    }

    public void save(
                final ConversionRequest request,
                final ConversionResponse response) throws JsonProcessingException {

        final VideoConversions conversion = new VideoConversions(
                                                    response.getUuid().toString(),
                                                    request.getPath().toString(),
                                                    "");

        AmazonDynamoDB client = AmazonDynamoDBClientBuilder.standard()
                .withRegion(Regions.US_EAST_2)
                .build();
        DynamoDB dynamoDB = new DynamoDB(client);
        Table table = dynamoDB.getTable("video_conversion");
        Item item = new Item()
                .withPrimaryKey("uuid", conversion.getUuid().toString())
                .withString("origin_path", conversion.getOriginPath().toString())
                .withString("target_path", "test")
                .withString("conversion_status", "EN_COURS");

        PutItemOutcome outcome = table.putItem(item);
        //log.info("DB outcome = {}", outcome.getPutItemResult().getSdkHttpMetadata().toString());

        final Message message = new Message(conversion.toJson().getBytes(), new MessageProperties());
        rabbitTemplate.convertAndSend(conversionExchange, conversionQueue,  conversion.toJson());
    }

}
