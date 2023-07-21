#!/bin/bash


function test_add()
{
    local result=$(($1 + $2))
    echo "$result"
}



function test_mult
{
    local result=$(($1 * $2))
    echo "$result"
}


function test_div(){
    local result=$(($1 / $2))
    echo "$result"
}


function test_sub{
    local result=$(($1 - $2))
    echo "$result"
}