# Variante 2 : build multi-stage, aucun JDK requis sur la machine
# JAVA_VERSION doit correspondre à la version Java choisie sur start.spring.io (17, 21 ou 25)
ARG JAVA_VERSION=17

# ---------- Étape 1 : compilation ----------
FROM eclipse-temurin:${JAVA_VERSION}-jdk AS build
WORKDIR /workspace

# Fichiers Gradle d'abord (cache des dépendances)
COPY gradlew settings.gradle build.gradle ./
COPY gradle ./gradle
# Corrige les fins de ligne Windows (CRLF) et le bit exécutable perdu au dézippage sous Windows
RUN sed -i 's/\r$//' gradlew && chmod +x gradlew
RUN --mount=type=cache,target=/root/.gradle ./gradlew --no-daemon dependencies > /dev/null

# Puis le code source
COPY src ./src
RUN --mount=type=cache,target=/root/.gradle ./gradlew --no-daemon bootJar

# ---------- Étape 2 : exécution ----------
FROM eclipse-temurin:${JAVA_VERSION}-jre
WORKDIR /app
RUN useradd --system --uid 1001 spring
USER spring
COPY --from=build --chown=spring:spring /workspace/build/libs/*-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
