import Data.Char

---------------------------------- Factorial ----------------------------------
-- fact 10 --> 55

fact :: Int -> Int
fact 0 = 0
fact n = n + fact (n - 1)

----------------------------- Fibonacci? Why not. -----------------------------
-- fib 0 --> 0
-- fib 1 --> 1
-- fib 2 --> 1
-- fib 3 --> 2
-- fib 6 --> 8

fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n - 1) + fib (n - 2)

----------------------------------- Ordinal -----------------------------------
-- The algorithm here is "borrowed" from Rails ActiveSupport's "ordinal" and 
-- "ordinalize" methods, see:
-- http://api.rubyonrails.org/classes/ActiveSupport/Inflector.html
--
-- ordinal 24 --> "24th"
-- ordinal 2 --> "2nd"

ordinal :: Int -> String
ordinal n
    | n == 11 || 
      n == 12 || 
      n == 13     = numword ++ "th" -- Three exceptions.
    | absnum == 1 = numword ++ "st"
    | absnum == 2 = numword ++ "nd"
    | absnum == 3 = numword ++ "rd"
    | otherwise   = numword ++ "th"
    where absnum = n `mod` 10
          numword = (show n)

---------------------------------- Pig Latin ----------------------------------
-- Maybe not the best overall Pig Latin translator in the whole wide world, but
-- not bad for 15 minutes.
--
-- piglatin "don't say ice cream" --> "on'tday aysay ceiay reamcay"

piglatin' :: String -> String
piglatin' word 
    | prefix == "th" ||
      prefix == "qu" = remainder ++ prefix ++ "ay"
    | otherwise = tail word ++ [head word] ++ "ay"
    where prefix    = take 2 word
          remainder = drop 2 word

piglatin :: String -> String
piglatin sentence = unwords [ piglatin' word | word <- words sentence ]

--------------------------------- Palindrome ----------------------------------
-- There might be more Haskell-ish ways to do some parts of this, but overall
-- I'm very pleased.
--
-- palindrome "abcdef" --> False
-- palindrome "A man, a plan, a canal, Panama!" --> True

collapse :: String -> String
collapse string = filter isLetter (map toLower string)

palindrome :: String -> Bool
palindrome sentence
    | length stringy == 0 || length stringy == 1 = True
    | otherwise = head stringy == last stringy && palindrome trimmed
    where stringy = collapse sentence
          trimmed = tail (init stringy)

-- vim: set ts=4 sw=4 et :
