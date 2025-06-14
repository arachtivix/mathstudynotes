(ns proj.shared-test
  #_{:clj-kondo/ignore [:refer-all]}
  (:require [clojure.test :refer :all]
            [proj.shared :refer :all]))

(deftest test-get-seq-before-repeat
  (testing "mixes of repeats, no repeats, empties"
    (is (= '(1 2 3) (get-seq-before-repeat '(1 2 3 3))))
    (is (= '(1 2 3) (get-seq-before-repeat '(1 2 3 3 2 1))))
    (is (= '(1) (get-seq-before-repeat '(1 1))))
    (is (= '() (get-seq-before-repeat '())))
    (is (= '(1) (get-seq-before-repeat '(1))))))

(deftest test-find-next-prime-vec
  (testing "find-next-prime-vec"
    (is (= [2] (find-next-prime-vec [])))
    (is (= [2 3] (find-next-prime-vec [2])))
    (is (= [2 3 5] (find-next-prime-vec [2 3])))
    (is (= [2 3 5 7 11 13] (find-next-prime-vec [2 3 5 7 11])))))

(deftest test-prime-seq
  (testing "test the primes"
    (is (= [2] (take 1 prime-seq)))
    (is (= [2 3] (take 2 prime-seq)))
    (is (= [2 3 5 7 11] (take 5 prime-seq)))))