package es.codeurjc.commitclassifier.controller;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;

import es.codeurjc.commitclassifier.model.CommitClassificationResult;
import es.codeurjc.commitclassifier.repositories.CommitClassificationResultRepository;
import io.github.bonigarcia.wdm.WebDriverManager;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class CommitControllerTest {

    @Autowired
    private CommitClassificationResultRepository commitClassificationResultRepository;

    @LocalServerPort
    int port;

    private WebDriver driver;

    @BeforeAll
    public static void setupClass() {
        WebDriverManager.chromedriver().setup();
    }

    @BeforeEach
    public void setupTest() {
        ChromeOptions options = new ChromeOptions();
        // options.addArguments("--headless");
        this.driver = new ChromeDriver(options);
    }

    @AfterEach
    public void teardown() {
        if (this.driver != null) {
            this.driver.quit();
        }
    }

    @Test
    void testCreateCommitClassificationResult() throws InterruptedException {

        // CREATE A COMMIT CLASSIFICATION RESULT (EXAMPLE)
        CommitClassificationResult resultExample = new CommitClassificationResult(
            "ddec8ed2d4905d0967ce2ec432e440e582aa52c6",
            "Michel", 
            "true", 
            "false", 
            "true", 
            "Timing and execution", 
            "A comment", 
            true
        );

        this.driver.get("http://localhost:" + this.port + "/commit/1");

        this.driver.findElement(By.name("reviewer")).sendKeys(resultExample.getReviewer());
        this.driver.findElement(By.name("is_bug_fixing_commit")).sendKeys(resultExample.getIs_bug_fixing_commit());
        this.driver.findElement(By.name("is_obvious_bug")).sendKeys(resultExample.getIs_obvious_bug());
        this.driver.findElement(By.name("is_safety_related")).sendKeys(resultExample.getIs_safety_related());
        this.driver.findElement(By.name("type_of_safety_related")).sendKeys(resultExample.getType_of_safety_related());
        this.driver.findElement(By.name("comment")).sendKeys(resultExample.getComment());
        this.driver.findElement(By.name("link_visited")).click();

        this.driver.findElement(By.name("submit")).click();

        // CHECK THAT THE MESSAGE IS DISPLAYED
        String message = this.driver.findElement(By.id("message-header")).getText();
        assertEquals("Your classification has been saved!", message);

        // CHECK THAT THE COMMIT CLASSIFICATION RESULT IS CREATED AND PERSIST
        CommitClassificationResult result =  commitClassificationResultRepository.findById(1L).orElseThrow();
        assertEquals(resultExample.getCommit_hash(), result.getCommit_hash());
        assertEquals(resultExample.getReviewer(), result.getReviewer());
        assertEquals(resultExample.getIs_bug_fixing_commit(), result.getIs_bug_fixing_commit());
        assertEquals(resultExample.getIs_obvious_bug(), result.getIs_obvious_bug());
        assertEquals(resultExample.getIs_safety_related(), result.getIs_safety_related());
        assertEquals(resultExample.getType_of_safety_related(), result.getType_of_safety_related());
        assertEquals(resultExample.getComment(), result.getComment());
        assertEquals(resultExample.isLink_visited(), result.isLink_visited());
        
    }

}
