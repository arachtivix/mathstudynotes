# Automated Releases

This repository is configured with GitHub Actions to automatically create releases when changes are pushed to the `main` branch.

## What Gets Released

Each release includes JAR files for the following Clojure projects:
- **project_euler/proj** - Project Euler solutions
- **winning_ways/cutcake** - Winning Ways cutcake project
- **unbound/hand_numbers** - Hand numbers project
- **cloj-brv-tru/ch1/clojure-noob** - Clojure noob project

## Workflow Process

1. When code is pushed to the `main` branch, the workflow triggers
2. Java 17 and Leiningen are installed
3. Each project is:
   - Dependencies are installed (`lein deps`)
   - Tests are run (`lein test`)
   - JAR files are built (`lein uberjar`)
4. If all tests pass, a new release is created with:
   - A timestamp-based tag (e.g., `release-20240115-143022`)
   - All standalone JAR files as release assets

## Using JAR Files as Dependencies

To use these JAR files as dependencies in another GitHub repository:

### Option 1: Direct Download
Download the JAR files from the [Releases page](https://github.com/arachtivix/mathstudynotes/releases) and add them to your project's library path.

### Option 2: Leiningen Project
In your `project.clj`, you can reference the JAR files from a release:

```clojure
(defproject your-project "0.1.0"
  :dependencies [[org.clojure/clojure "1.11.1"]]
  :resource-paths ["lib/project-euler-proj.jar"
                   "lib/winning-ways-cutcake.jar"])
```

### Option 3: Maven/Gradle
For Maven or Gradle projects, you can install the JAR files to your local Maven repository:

```bash
mvn install:install-file \
  -Dfile=project-euler-proj.jar \
  -DgroupId=mathstudynotes \
  -DartifactId=project-euler-proj \
  -Dversion=0.1.0-SNAPSHOT \
  -Dpackaging=jar
```

## Workflow Configuration

The workflow is defined in `.github/workflows/release.yml` and:
- Triggers on pushes to the `main` branch
- Requires all tests to pass before creating a release
- Uses the `softprops/action-gh-release` action to create releases
- Generates unique release tags based on timestamps

## Modifying the Workflow

To add or remove projects from the release:
1. Edit `.github/workflows/release.yml`
2. Add/remove build steps for the project
3. Update the `files:` section in the release step
4. Update the release body to reflect the changes
