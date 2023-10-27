import os
import time
from flask import Flask, render_template, send_from_directory, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/capture")
def capture():
    image_filenames = capture_images()  # capture_images 함수를 호출하여 이미지 파일 이름 목록을 가져옴
    return jsonify(
        {"status": "success", "image_filenames": image_filenames}
    )  # JSON 응답을 반환


def capture_images():
    from picamera import PiCamera  # picamera 모듈을 사용하여 Raspberry Pi 카메라를 제어

    image_filenames = []  # 이미지 파일 이름을 저장할 리스트 초기화
    timestamp = int(time.time())  # 현재 시간을 기반으로 타임스탬프 생성

    with PiCamera() as camera:  # PiCamera 객체를 생성하고 사용한 후 자동으로 종료
        camera.resolution = (250, 250)  # 사진 크기 조절

        for i in range(4):
            image_filename = f"captured_{timestamp}_{i}.jpg"  # 이미지 파일 이름 생성
            image_filenames.append(image_filename)  # 생성된 파일 이름을 리스트에 추가
            camera.start_preview()  # 미리보기 시작
            time.sleep(2)  # 워밍업 시간 2초
            camera.capture(f"images/{image_filename}")  # 이미지를 캡처하여 'images' 디렉토리에 저장
            camera.stop_preview()  # 미리보기 종료
            time.sleep(5)  # 5초 대기 후 다음 사진 촬영

    return image_filenames  # 캡처된 이미지 파일 이름 목록 반환


@app.route("/images/<filename>")
def get_image(filename):
    return send_from_directory("images", filename)  # 'images' 디렉토리에서 요청된 이미지 파일을 반환


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
