<?php


//  1 020 0(1|0)0



class Code {

  protected $code;

  protected $result;

  protected $decale;

  protected $encrypted;

  public function generate(){
    $this->result = mt_rand (0, 1);
    $this->code = intval('1'.mt_rand (0, 9).'2'.mt_rand (0, 9).mt_rand (0, 9).$this->result.mt_rand (0, 9));
    return $this->code;
  }

  public function getCode() {
    return $this->code;
  }

  public function getDecale() {
    return $this->decale;
  }

  public function getResult() {
    return $this->result;
  }

  public function getEncrypted() {
    return $this->encrypted;
  }

  public function encrypt() {
    $this->decale = mt_rand (1, 9);
    $code_in_binary = decbin($this->code);

    $index = 0;
    while($index < $this->decale) {
      $code_in_binary .= strval(mt_rand (0,1));
      $index++;
    }
    $this->encrypted = bindec($code_in_binary).$this->decale;
  }

  public function decrypt($encrypted) {
    $decale = intval(substr($encrypted, -1, 1));
    $decrypt = substr($encrypted, 0, strlen($encrypted)-1);

    $binary_string = decbin(intval($decrypt));
    $code = substr($binary_string, 0, strlen($binary_string)-$decale);

    return bindec($code);
  }

}

$code = new Code();

$index = 0;
$data = [];
while ($index < 100000) {
  $code->generate();
  $code->encrypt();

  $encrypted = $code->getEncrypted();

  $code_decrypthed = $code->decrypt($encrypted);

  // If no FALSE has been displayed, so the decrypt task could be done.
  if ($code_decrypthed !== $code->getCode()) {
    var_dump(FALSE);
  }

  $result = $code->getResult();
  $data[$encrypted] = [
    $encrypted,
    $result,
  ];
  $index++;
}


$file = fopen("data.csv","w");

foreach ($data as $line){
  fputcsv($file, $line);
}

fclose($file);

var_dump(count($data));

