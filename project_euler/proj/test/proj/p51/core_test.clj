(ns proj.p51.core-test
  (:require [clojure.test :refer [deftest is testing]]
            [proj.p51.core :refer [all-n-digit-primes all-n-digit-masks
                                   combine-int-with-mask numbers-under-mask-all-same?
                                   num-to-masked]]))

(deftest test-all-n-digit-primes
  (testing "all-n-digit-primes"
    (is (= [2 3 5 7] (all-n-digit-primes 1)))
    (is (= [11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97] (all-n-digit-primes 2)))))

(deftest test-all-n-digit-masks
  (testing "all-n-digit-masks"
    (is (= ["X" "O"] (all-n-digit-masks 1)))
    (is (= ["XX" "XO" "OX" "OO"] (all-n-digit-masks 2))
    (is (= ["XXX" "XXO" "XOX" "XOO" "OXX" "OXO" "OOX" "OOO"] (all-n-digit-masks 3))))))

(deftest test-numbers-under-mask-all-same?
  (testing "number-under-mask-all-same?"
    (is (= true (numbers-under-mask-all-same? 1 "X")))
    (is (= true (numbers-under-mask-all-same? 1223 "OXXO")))
    (is (= false (numbers-under-mask-all-same? 1223 "XOOX")))
    (is (= true (numbers-under-mask-all-same? 1223 "XOOO")))
    (is (= true (numbers-under-mask-all-same? 1111 "XXXX")))
    (is (= false (numbers-under-mask-all-same? 1223 "XXXX")))))

(deftest test-combine-int-with-mask
  (testing "combine-int-with-mask"
    (is (= "X" (combine-int-with-mask 1 "X")))
    (is (= "1" (combine-int-with-mask 1 "O")))
    (is (= "X2" (combine-int-with-mask 12 "XO")))
    (is (= "2X" (combine-int-with-mask 29 "OX")))
    (is (= "75" (combine-int-with-mask 75 "OO")))))

(deftest test-num-to-masked
  (testing "num-to-masked"
    (is (= "X" (num-to-masked 1 "X")))
    (is (= "1" (num-to-masked 1 "O")))
    (is (= "1X" (num-to-masked 12 "OX")))
    (is (= "X2" (num-to-masked 12 "XO")))
    (is (= "12" (num-to-masked 12 "OO")))))