<?php
$url = "https://play.pokemonshowdown.com/sprites/gen5/{$argv[1]}.png"; // URL of the image you want to grab
// $localPath = "pksprites/{$argv[1]}.png"; // Local path where you want to save the image

// Get the image contents from the URL
$imageData = @file_get_contents($url);

if ($imageData !== false) {
    // Save the image contents to a local file
    // $success = file_put_contents($localPath, $imageData);
    echo "0";
} else {
    echo "1"; // Failure signal
}
?>