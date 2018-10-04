<?php

require_once __DIR__ . '/../vendor/autoload.php';

use Symfony\Component\Yaml\Yaml;

$countries = scandir('Countries');

foreach( $countries as $country) {
    if ( $country == '.' ) { continue; }
    if ( $country == '..' ) { continue; }
    if ( $country == '.common' ) { continue; }

    $files = scandir('Countries/' . $country);
    foreach( $files as $file) {
        $file_parts = pathinfo($file);
        if ( $file_parts['extension'] != 'yaml') { continue; }
        print 'Validating ' . $country . '/' . $file . "\n";
        Yaml::parseFile(__DIR__  . '/../' . 'Countries/' .$country . '/' . $file);
    }
}
?>
