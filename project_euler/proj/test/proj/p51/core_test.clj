(ns proj.p51.core-test
  (:require [clojure.test :refer [deftest is testing]]
            [proj.p51.core :refer [all-n-digit-primes]]))

(deftest test-all-n-digit-primes
  (testing "all-n-digit-primes"
    (is (= [2 3 5 7] (all-n-digit-primes 1)))
    (is (= [11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97] (all-n-digit-primes 2)))))