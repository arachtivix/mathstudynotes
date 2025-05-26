(ns proj.p206.core-test
  (:require [clojure.test :refer :all]
            [proj.p206.core :refer :all]))

(deftest dec-exp-int-test
  (testing "Testing decimal expansion of integers"
    (is (= '(1 0 0 0) (dec-exp-int 1000)))
    (is (= '(1 2 3 4) (dec-exp-int 1234)))
    (is (= '(0) (dec-exp-int 0)))))

(deftest matches-pattern-test
  (testing "Testing matches pattern"
    (is (= true (matches-pattern? '(1 :_ 3 :_) '(1 2 3 4))))
    (is (= false (matches-pattern? '(1 :_ 2 :_) '(1 2 3 4))))
    (is (= false (matches-pattern? '(1 :_ 3 :_) '(1 2 3 4 5))))))

(deftest dec-exp-to-bigint-test
  (testing "Testing decimal expansion to bigint"
    (is (= 1234 (dec-exp-to-bigint '(1 2 3 4))))
    (is (= 0 (dec-exp-to-bigint '())))
    (is (= 999999999999999999999999999999 (dec-exp-to-bigint (take 30 (repeat 9)))))))

(deftest pat-min-test
  (testing "Testing pattern minimum value function"
    (is (= 1030 (patt-min '(1 :_ 3 :_))))
    (is (= 0 (patt-min '(:_ :_ :_ :_))))
    (is (= 1234 (patt-min '(1 2 3 4))))))

(deftest pat-max-test
  (testing "Testing pattern minimum value function"
    (is (= 1939 (patt-max '(1 :_ 3 :_))))
    (is (= 9999 (patt-max '(:_ :_ :_ :_))))
    (is (= 1234 (patt-max '(1 2 3 4))))))

(deftest brute-force-generalized-test
  (testing "Testing the brute force approach generalized"
    (is (= '(4) (brute-force-generalized '(1 :_))))))