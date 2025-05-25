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
    (is (= true (matches-pattern? '(1 :_ 3 :_) '(1 2 3 4)))))
    (is (= false (matches-pattern? '(1 :_ 2 :_) '(1 2 3 4))))
    (is (= false (matches-pattern? '(1 :_ 3 :_) '(1 2 3 4 5)))))