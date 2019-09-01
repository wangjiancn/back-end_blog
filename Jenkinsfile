pipeline {
    agent none
    environment {
        CI = 'true'
    }
    stages {
        stage('Build') {
            agent any
            steps{
                script{
                    def date = new Date().format("YYYYMMdd")    // 获取一个 20190101 格式的时间字符串
                    def commit = env.GIT_COMMIT
                    def short_commit = commit ? commit[0..6] : "" // 取前6为git sha
                    def local_tag = date + "-" + short_commit   // 20190101-d234k4
                    docker.withRegistry("https://${env.DOCKER_REG_ALI}", "docker") {
                        project_image = docker.build("${env.DOCKER_REG_ALI}/blog-backend:${local_tag}")
                    }
                }
            }
        }
        stage('Push') {
            agent any
            when { tag "*" }    // 如果有tag推送镜像,没有则跳过
            steps {
                script{
                    def tag = sh(returnStdout: true, script: "git tag -l --points-at HEAD").trim() // 获取tag
                    println tag
                    def major = tag.split('\\.')[0]
                    if(tag){
                        docker.withRegistry("https://${env.DOCKER_REG_ALI}", "docker") {
                            project_image.push(tag)
                            project_image.push(major)
                            project_image.push("latest")
                        }
                    }
                    production_image = env.DOCKER_REG_ALI + ":" + tag
                }
                sh "echo Deploy completed"
            }
        }
    }
}