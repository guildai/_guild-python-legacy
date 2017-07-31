import argparse
import sys
import time

def init_flags():
    global FLAGS
    parser = argparse.ArgumentParser()
    parser.add_argument("--rundir", default="/tmp/MNIST_train")
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--train-time", type=int, default=5)
    parser.add_argument("--simulate-error", type=int, default=None)
    FLAGS, _ = parser.parse_known_args()

def main():
    if FLAGS.simulate_error:
        error()
    elif FLAGS.prepare:
        prepare()
    elif FLAGS.train:
        train()

def error():
    sys.stderr.write("ERROR!\n")
    sys.exit(FLAGS.simulate_error)

def prepare():
    print("Preparing")

def train():
    stop = time.time() + FLAGS.train_time
    while time.time() < stop:
        print("Training...")
        time.sleep(1)
    print("Done")

def evaluate():
    print("Evaluating")

if __name__ == "__main__":
    init_flags()
    main()
