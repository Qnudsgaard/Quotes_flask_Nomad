job "quotes-flask-backend" {
  type = "service"

  group "quotes-flask-backend" {
    count = 1
    network {
      port "web" {
        static = 5000
      }
    }

    service {
      name     = "backend-service"
      port     = "web"
      provider = "nomad"
    }

    task "ptc-web-task" {
      template {
        data        = <<EOH

EOH
        destination = "local/env.txt"
        env         = true
      }

      driver = "docker"

      config {
        image = "muhamadsdu/backend:latest"
        ports = ["web"]
      }
    }
  }
}