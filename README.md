# Medol

This is the Medol project.

## Prerequisites

* Python >= 3.12
* Docker and Docker Compose
* Poetry

## Installation

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd medol
   ```

2. Install dependencies with Poetry:

   ```bash
   poetry install
   ```

3. Set up environment variables:

   * Create a `.env` file in the project root with necessary configurations.

## Running with Docker

### Start Database

```bash
make db-up
```

### Run Migrations

```bash
make migrate-up
```

### Run Development Server

```bash
make run-dev
```

### Run Server

```bash
make run
```

### Stopping and Cleaning Database

```bash
make db-down
```

### Access Database Container Bash

```bash
make db-bash
```

### Viewing Database Logs

```bash
make db-logs
```
