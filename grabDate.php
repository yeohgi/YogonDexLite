<?php
//grabBasic.php is used to grab the most recent folder/month smogon uploaded https://www.smogon.com/stats/, it writes the contents of https://www.smogon.com/stats/ to a temporary file called temp0.txt which is read from in smogon.py to extract the most recent folder.
$url = "https://www.smogon.com/stats/";
$localFilePath = "./temp0.txt";
$fileContent = file_get_contents($url);
if ($fileContent !== false) {
    $bytes_written = file_put_contents($localFilePath, $fileContent);
    if ($bytes_written !== false) {
        echo "File copied successfully to {$localFilePath}";
    } else {
    echo "Failed to write the file locally.";
    }
} else {
    echo "Failed to fetch the file from the URL.";
}
?>