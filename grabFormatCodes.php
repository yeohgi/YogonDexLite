<?php
//grabFormatCode is used to get all formats in a folder, useful to check if a format proposed by the user exists and for providing the user with real formats. Stores html contents of https://www.smogon.com/stats/{$argv[1]}/ to a file named temp1.txt which is processed in smogon.py, where argv[1] is a folder/date retrived using grabDate.
//arg1 = folder/date
$url = "https://www.smogon.com/stats/{$argv[1]}/";
$localFilePath = "./temp1.txt";
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