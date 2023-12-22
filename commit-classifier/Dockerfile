FROM maven:3.9.0-eclipse-temurin-17 as builder

WORKDIR /project

COPY pom.xml /project/

RUN mvn -B clean verify

COPY /src /project/src

RUN mvn -B -o package -DskipTests

FROM eclipse-temurin:17-jdk

WORKDIR /usr/src/app/

COPY --from=builder /project/target/*.jar /usr/src/app/app.jar

EXPOSE 8080

CMD [ "java", "-jar", "-Dspring.profiles.active=production", "app.jar" ]