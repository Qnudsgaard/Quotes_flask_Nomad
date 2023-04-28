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
FLASK_APP=app.py
FLASK_ENV=development
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
        BACKEND_HOST = "{{ range service \"backend\" }}{{ .Address }}{{ end }}"
        BACKEND_PORT = "{{ range service \"backend\" }}{{ .Port }}{{ end }}"
      }
    }
  }
}


