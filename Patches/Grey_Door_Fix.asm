LoROM
org $84BE44 : DW DoorUnlockTable
org $84BE4B
;DoorUnlockTable: DW $BDD4,$BDE3,$BDF2,$BE01,$BE1C,$BE1F,$BE30
              
org $84EFE0 
DoorUnlockTable: DW $BDD4,$BDE3,$BDF2,$BE01,$BE1C,$BE1F,$BE30
                 DW Kraid,Phantoon,Draygon,Ridley
Kraid: LDA #$0048 : JMP $BE33
Phantoon: LDA #$0058 : JMP $BE33
Draygon: LDA #$0060 : JMP $BE33
Ridley: LDA #$0050 : JMP $BE33
