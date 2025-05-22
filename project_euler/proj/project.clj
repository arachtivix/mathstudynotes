(defproject proj "0.1.0-SNAPSHOT"
  :description "Project Euler solutions in Clojure"
  :url "https://projecteuler.net/"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.11.1"]
                 [org.clojure/math.numeric-tower "0.0.5"]  ; For mathematical functions
                 [org.clojure/math.combinatorics "0.1.6"]] ; For combinatorics operations
  :main nil  ; No single main namespace as each problem has its own
  :aot :all
  :profiles {:dev {:dependencies [[org.clojure/test.check "1.1.1"]]}} ; For property-based testing
  :repl-options {:init-ns proj.core}
  :source-paths ["src"]
  :test-paths ["test"])
