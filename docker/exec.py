import subprocess
import sys

def get_container_id(image_name):
    # Get the list of running containers
    output = subprocess.check_output("docker ps", shell=True, text=True)

    # Split the output into lines
    lines = output.strip().split('\n')

    # Iterate through lines and find the container with the specified image name
    for line in lines[1:]:
        parts = line.split()
        if image_name in parts:
            return parts[0]

    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python docker_exec.py <image_name>")
        sys.exit(1)

    image_name = sys.argv[1]
    container_id = get_container_id(image_name)

    if container_id is None:
        print(f"No running container found for image '{image_name}'")
        sys.exit(1)

    # Run the docker exec command to start the bash prompt in the container
    subprocess.run(f"docker exec -it {container_id} /bin/bash", shell=True)

if __name__ == "__main__":
    main()
