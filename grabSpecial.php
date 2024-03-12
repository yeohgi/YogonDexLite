<?php
//arg1 = date
//arg2 = special folder
//arg3 = .txt
$url = "https://www.smogon.com/stats/{$argv[1]}/{$argv[2]}/{$argv[3]}";
$localFilePath = "prepro/{$argv[1]}/{$argv[2]}/{$argv[3]}";
$fileContent = file_get_contents($url);
if ($fileContent !== false) {
    // Use file_put_contents to save the content to a local file
    $bytes_written = file_put_contents($localFilePath, $fileContent);
    // Check if the write operation was successful
    if ($bytes_written !== false) {
        echo "File copied successfully to {$localFilePath}";
    } else {
        echo "Failed to write the file locally.";
    }
} else {
    echo "Failed to fetch the file from the URL.";
}
?>