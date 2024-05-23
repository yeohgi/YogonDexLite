<?php
//grabBasic.php is used to grab basic .txt files in folders sorted by date on https://www.smogon.com/stats/, .txt files contained in deeper folders are grabbed using grabSpecial.php.
$url = "https://www.smogon.com/stats/{$argv[1]}/{$argv[2]}";
$localFilePath = "prepro/{$argv[1]}/{$argv[2]}";
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