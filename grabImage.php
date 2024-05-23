<?php
//grabImage.php is used to determine whether a pokemon image name is valid.
$url = "https://play.pokemonshowdown.com/sprites/gen5/{$argv[1]}.png";

// $localPath = "pksprites/{$argv[1]}.png";

$imageData = @file_get_contents($url);

if ($imageData !== false) {
    //file_put_contents($localPath, $imageData);
    echo "0";
    //valid image name
} else {
    echo "1";
    //not valid image name
}
//can uncomment commented code to be able to save the image
?>

