import argparse
import time

def init_flags():
    global FLAGS
    parser = argparse.ArgumentParser()
    parser.add_argument("--rundir", default="/tmp/MNIST_train")
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--train_time", type=int, default=0)
    FLAGS, _ = parser.parse_known_args()

def main():
    if FLAGS.prepare:
        prepare()
    elif FLAGS.train:
        train()

def prepare():
    print("TODO: prepare")

def train():
    stop = time.time() + FLAGS.train_time
    while time.time() < stop:
        print("Training...")
        time.sleep(1)
    print("Done")

def evaluate():
    print("TODO: evaluate")

if __name__ == "__main__":
    init_flags()
    main()
