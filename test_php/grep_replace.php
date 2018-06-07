<?php

$string = 'google 123, 456';
$pattern = '/o/i';
$replacement = 'x';
echo preg_replace($pattern, $replacement, $string);

?>
