<?php

 $AES_KEY = '...';
 $TOKEN = '...';

 $key = '2Wq7)qkX~cp7)H|n_tc&o+:G_USN3/-uIi~>M+c ;Oq]E{t9)RC_5|lhAA_Qq%_4';
 $PRIVATE_KEY = 2615678;
 $time = time();

 $number="+...";



function decrypt($key, $garble) {
   
   return openssl_decrypt(
    base64_decode($garble),
    "aes-256-ecb",
    $key,
    OPENSSL_RAW_DATA
);

}


function encrypt($key, $garble) {
   
 $method = 'AES-256-ECB';
    $ivSize = openssl_cipher_iv_length($method);
    $iv = openssl_random_pseudo_bytes($ivSize);
   return openssl_encrypt(
    $garble,
    "aes-256-ecb",
    $key,
    OPENSSL_RAW_DATA
);

}

function Send_Post($post_url, $post_data,$signature)
 { global $TOKEN,$time;
  
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $post_url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 

 if ($post_data!=""){
  curl_setopt($ch, CURLOPT_POST, 1);
  curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
  }
  
 curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);

 curl_setopt($ch, CURLOPT_HTTPHEADER, array(
 "X-App-Version: 4.9.1",
 "X-Token: ".$TOKEN,
 "X-Os: android 5.0",
 "X-Client-Device-Id: 14130e29cebe9c39",
 "Content-Type: application/json; charset=utf-8",
 "Accept-Encoding: deflate",
 "X-Req-Timestamp: ".$time,
 "X-Req-Signature: ".$signature,
 "X-Encrypted: 1"));

 curl_setopt ($ch, CURLOPT_TIMEOUT, 60);
 
 $data = curl_exec($ch);
 curl_close($ch);

 return $data;
}




function GetByPhone ($phone) {

 global $time, $TOKEN, $key, $AES_KEY;

 $req='{"countryCode":"RU","source":"search","token":"'.$TOKEN.'","phoneNumber":"'.$phone.'"}';
 
 $string = ($time.'-'.$req);

 $signature= base64_encode(hash_hmac ( 'sha256' , $string , $key , true ));

 $crypt_data=base64_encode(encrypt(hex2bin($AES_KEY), $req));

 $zprs =Send_Post("https://pbssrv-centralevents.com/v2.5/search", '{"data":"'.$crypt_data.'"}',$signature);

 $zprs=json_decode($zprs);

 $time = time();

 return $zprs->data;

 }



 function GetByPhoneTags ($phone) {

 global $time, $TOKEN, $key, $AES_KEY;

 $req='{"countryCode":"RU","source":"details","token":"'.$TOKEN.'","phoneNumber":"'.$phone.'"}';

 $string = ($time.'-'.$req);

 $signature= base64_encode(hash_hmac ( 'sha256' , $string , $key , true ));

 $crypt_data=base64_encode(encrypt(hex2bin($AES_KEY), $req));

 $zprs =Send_Post("https://pbssrv-centralevents.com/v2.5/number-detail", '{"data":"'.$crypt_data.'"}',$signature);

 $zprs=json_decode($zprs);

 return $zprs->data;

 }


 print_r(json_decode(decrypt(hex2bin($AES_KEY), GetByPhone($number))));
 echo "\n\n\n";
 print_r(json_decode(decrypt(hex2bin($AES_KEY), GetByPhoneTags($number))));



?>
