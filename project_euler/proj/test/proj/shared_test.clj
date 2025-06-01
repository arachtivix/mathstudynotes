(ns proj.shared-test
  (:require [clojure.test :refer :all]
            [proj.shared :refer :all]))

(deftest test-get-seq-before-repeat
  (testing "mixes of repeats, no repeats, empties"
    (is (= '(1 2 3) (get-seq-before-repeat '(1 2 3 3))))
    (is (= '(1 2 3) (get-seq-before-repeat '(1 2 3 3 2 1))))
    (is (= '(1) (get-seq-before-repeat '(1 1))))
    (is (= '() (get-seq-before-repeat '())))
    (is (= '(1) (get-seq-before-repeat '(1))))))