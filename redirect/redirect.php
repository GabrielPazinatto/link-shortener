<?php
$api_url = "shortify.rf.gd";

$short_url = trim($_SERVER['REQUEST_URI'], '/');

if (!empty($short_url)) {
    $redirect_url = "$api_url/$short_url";
    header("Location: $redirect_url");
    exit();
} else {
    echo "URL Not Found.";
}
?>
