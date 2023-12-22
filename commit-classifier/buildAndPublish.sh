mvn spring-boot:build-image -DskipTests
docker push maes95/commit-classifier:$(mvn -q help:evaluate -Dexpression=project.version -DforceStdout)