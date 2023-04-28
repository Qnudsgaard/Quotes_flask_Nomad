job "quotes-flask-web" {
  type = "service"

  group "quotes-flask-web" {
    count = 1
    network {
      port "web" {
        static = 5000
      }
    }

    service {
      name     = "frontend-service"
      port     = "web"
      provider = "nomad"
    }

    task "ptc-web-task" {
      template {
        data        = <<EOH
        FLASK_HOST={{ env "BACKEND_HOST" }}
        FLASK_PORT={{ env "BACKEND_PORT" }}
EOH
        destination = "local/env.txt"
        env         = true
      }

      driver = "docker"

      config {
        image = "muhamadsdu/frontend:latest"
        ports = ["web"]
      }

      env {
        BACKEND_HOST = "{{ range service \"quotes-flask-backend\" }}{{ .Address }}{{ end }}"
        BACKEND_PORT = "{{ range service \"quotes-flask-backend\" }}{{ .Port }}{{ end }}"
      }
    }
  }
}


