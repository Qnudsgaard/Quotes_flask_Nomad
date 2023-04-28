job "quotes-flask-setup" {
  type = "batch"

  group "quotes-flask-setup" {
    count = 1

    task "quotes-flask-setup-task" {

      template {
        data        = <<EOH
{{ range nomadService "postgres-svc" }}
POSTGRES_HOST={{ .Address }}
POSTGRES_PORT={{ .Port }}
{{ end }}
EOH
        destination = "local/env.txt"
        env         = true
      }
      driver = "docker"

      config {
        image = "muhamadsdu/backend:latest"
      }
    }
  }
}