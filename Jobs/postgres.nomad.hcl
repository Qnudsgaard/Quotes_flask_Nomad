job "quotes-flask-postgres" {
  type = "service"

  group "qf-postgres" {
    count = 1
    network {
      port "postgres" {
        to = 5432
      }
    }

    service {
      name     = "postgres-svc"
      port     = "postgres"
      provider = "nomad"
    }


    task "postgres-task" {
      driver = "docker"

      env {
        POSTGRES_PASSWORD = "Y29tcGxpY2F0ZWQ="
      }

      config {
        image = "postgres:latest"
        ports = ["postgres"]
      }
    }
  }
}