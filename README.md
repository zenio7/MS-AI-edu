graph TD
    classDef main1 fill:#ff6b6b,stroke:#ff4757,stroke-width:3px,color:#fff
    classDef main2 fill:#4d79ff,stroke:#3742fa,stroke-width:3px,color:#fff
    classDef shared fill:#6bcf7f,stroke:#2ed573,stroke-width:2px,color:#fff
    classDef unique1 fill:#ffd93d,stroke:#ffa502,stroke-width:2px,color:#333
    classDef unique2 fill:#a8edea,stroke:#ff9ff3,stroke-width:2px,color:#333

    A[머신러닝]:::main1
    B[딥러닝]:::main2

    S0[데이터]:::shared
    A --> S0
    B --> S0
    S1[알고리즘]:::shared
    A --> S1
    B --> S1
    S2[예측]:::shared
    A --> S2
    B --> S2
    S3[모델]:::shared
    A --> S3
    B --> S3
    S4[훈련]:::shared
    A --> S4
    B --> S4
    S5[평가]:::shared
    A --> S5
    B --> S5
    S6[AI]:::shared
    A --> S6
    B --> S6

    U10[회귀분석]:::unique1
    A --> U10
    U11[분류]:::unique1
    A --> U11
    U12[클러스터링]:::unique1
    A --> U12
    U13[의사결정트리]:::unique1
    A --> U13
    U14[SVM]:::unique1
    A --> U14
    U15[랜덤포레스트]:::unique1
    A --> U15

    U20[신경망]:::unique2
    B --> U20
    U21[역전파]:::unique2
    B --> U21
    U22[CNN]:::unique2
    B --> U22
    U23[RNN]:::unique2
    B --> U23
    U24[LSTM]:::unique2
    B --> U24
    U25[Transformer]:::unique2
    B --> U25
