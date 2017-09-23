import learners as lrn

learnerBuilders = [
                    #lrn.LearnerBuilder.NaiveBayesLearnerBuilder, 
                    lrn.LearnerBuilder.DecisionStumpLearnerBuilder,
                    lrn.LearnerBuilder.HoeffdingAdaptiveLearnerBuilder,
                    #lrn.LearnerBuilder.HoeffdingOptionLearnerBuilder,
                    lrn.LearnerBuilder.HoeffdingLearnerBuilder,
                    #lrn.LearnerBuilder.OzaBagLearnerBuilder,
                    lrn.LearnerBuilder.OzaBoostLearnerBuilder,
                    #lrn.LearnerBuilder.AccuracyUpdatedEnsembleLearnerBuilder,
                    #lrn.LearnerBuilder.AccuracyWeightedEnsembleLearnerBuilder,
                    #lrn.LearnerBuilder.DriftDetectionMethodClassifierLearnerBuilder,
                    #lrn.LearnerBuilder.OzaBagAdwinLearnerBuilder,
                    #lrn.LearnerBuilder.OzaBoostAdwinLearnerBuilder,
                    #lrn.LearnerBuilder.HoeffdingAdaptiveLearnerBuilder
                    ] 

learners_1 = [
              r"-l trees.HoeffdingTree",
              r"-l (trees.HoeffdingTree -g 100 -c 0.01)",
          ]
learners_2 = [
              r"-l trees.HoeffdingTree",
              r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree)",
              r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d ADWINChangeDetector)",
              r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d SeqDrift2ChangeDetector)"
              ]

learners_2_1 = [
              r"-l trees.EFDT",
              r"-l trees.HoeffdingTree",
              r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree)",
              r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d ADWINChangeDetector)", 
              r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d ADWINMonotoneChangeDetector)",
              r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d SeqDrift2ChangeDetector)",
              r"-l trees.HoeffdingAdaptiveTree",
              r"-l trees.HoeffdingOptionTree"
              ]

learners_3_1 = [
              #r"-l trees.EFDT",
              r"-l trees.HoeffdingTree",
              r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree)",
              r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d ADWINMonotoneChangeDetector)",
              r"-l trees.HoeffdingAdaptiveTree",
              #r"-l trees.HoeffdingOptionTree"
              ]
 
temp = [
              r"-l (meta.OzaBoost -l (trees.HoeffdingTree -g 100 -c 0.01))",
              r"-l meta.AccuracyUpdatedEnsemble",

              r"-l (trees.HoeffdingAdaptiveTree -g 100 -c 0.01)",
              r"-l (meta.OzaBoost -l (trees.HoeffdingAdaptiveTree -g 100 -c 0.1)) ",
              r"-l (meta.AccuracyUpdatedEnsemble -l (trees.HoeffdingAdaptiveTree -g 100 -c 0.01))",

              r"-l (meta.OzaBoostAdwin -l (trees.HoeffdingTree -g 100 -c 0.01))",
              r"-l (meta.OzaBoostAdwin -l (trees.HoeffdingAdaptiveTree -g 100 -c 0.01))",

              r"-l (meta.OzaBoost -l trees.HoeffdingTree)"
              ]


report0 =    [

              # Plain Hoeffding Tree

              r"-l trees.HoeffdingTree",

              # Show AUE2 doesn't outperform OzaBoost once you match grace and split decision values

              r"-l (meta.OzaBoost -l (trees.HoeffdingTree -g 100 -c 0.01))",
              r"-l (meta.OzaBoost -l (trees.HoeffdingTree))",
              r"-l meta.OnlineAccuracyUpdatedEnsemble",

              # HAT-ADWIN base, normal default values

              r"-l (meta.OzaBoost -l (trees.HATADWIN))",
              r"-l (meta.OnlineAccuracyUpdatedEnsemble -l (trees.HATADWIN))",

              # Is this required?
              #r"-l (meta.OzaBoostAdwin -l (trees.HoeffdingTree -g 100 -c 0.01))",

              # Show how well HATADWIN does
              #r"-l (trees.HATADWIN) -g 100 -c 0.01)",
              r"-l (trees.HATADWIN)",
              r"-l (meta.OzaBoost -l (trees.HATADWIN -g 100 -c 0.1)) ",
              r"-l (meta.AccuracyUpdatedEnsemble -l (trees.HATADWIN -g 100 -c 0.01))",

              # Show OzaBoost is no beaten when wrapped with a change detector
              r"-l (drift.SingleClassifierDrift -l trees.HoeffdingTree -d ADWINMonotoneChangeDetector)",
              r"-l (drift.SingleClassifierDrift -l meta.OzaBoost -d ADWINMonotoneChangeDetector)",
              r"-l (drift.SingleClassifierDrift -l meta.AdaptableDiversityBasedOnlineBoosting -d ADWINMonotoneChangeDetector)",
              r"-l (drift.SingleClassifierDrift -l meta.BOLE -d ADWINMonotoneChangeDetector)",

              #r"-l (meta.OzaBoostAdwin -l (trees.HoeffdingAdaptiveTree -g 100 -c 0.01))",

              ]

temp_1 = [
 #               r"-l (meta.OzaBoost -l (trees.HATADWIN -g 100 -c 0.1)) ",
              r"-l (meta.OzaBoost -l (trees.HATADWIN))",
#                r"-l trees.HATADWIN ",
        ]

amnesia = [
              r"-l trees.HoeffdingTree",
              r"-l trees.VFDT",

              #r"-l (trees.VFDTGlobalWindow -W 25000)",
              r"-l (trees.VFDTGlobalWindow -W 50000)",
              #r"-l (trees.VFDTGlobalWindow -W 75000)",
              r"-l (trees.VFDTGlobalWindow -W 100000)",
              #r"-l (trees.VFDTGlobalWindow -W 125000)",
              #r"-l (trees.VFDTGlobalWindow -W 150000)",

              r"-l (trees.VFDTLeafWindow -W 1000)",
              #r"-l (trees.VFDTLeafWindow -W 5000)",
              #r"-l (trees.VFDTLeafWindow -W 10000)",
              #r"-l (trees.VFDTLeafWindow -W 12000)",
              #r"-l (trees.VFDTLeafWindow -W 13000)",
              r"-l (trees.VFDTLeafWindow -W 15000)",
              #r"-l (trees.VFDTLeafWindow -W 20000)",
              r"-l (trees.VFDTLeafWindow -W 25000)",
              #r"-l (trees.VFDTLeafWindow -W 999999)",

              r"-l (trees.VFDTLeafWindowADWIN -W 1000)",
              #r"-l (trees.VFDTLeafWindowADWIN -W 5000)",
              #r"-l (trees.VFDTLeafWindowADWIN -W 10000)",
              r"-l (trees.VFDTLeafWindowADWIN -W 15000)",
              #r"-l (trees.VFDTLeafWindowADWIN -W 20000)",
              #r" -l (trees.VFDTLeafWindowADWIN -W 25000)",
              r"-l (trees.VFDTLeafWindowADWIN -W 50000)",
              #r"-l (trees.VFDTLeafWindowADWIN -W 75000)",
              #r"-l (trees.VFDTLeafWindowADWIN -W 100000)",
              r"-l (trees.VFDTLeafWindowADWIN -W 125000)",
              r"-l (trees.VFDTLeafWindowADWIN -W 999999)",

              r"-l (trees.VFDTDecay -D 0.999999 -V -A)",
              #r"-l (trees.VFDTDecay -D 0.999995 -V -A)",
              r"-l (trees.VFDTDecay -D 0.99999 -V -A)",
              r"-l (trees.VFDTDecay -D 0.9999 -V -A)",
              r"-l (trees.VFDTDecay -D 0.999 -V -A)",
              r"-l (trees.VFDTDecay -D 0.99 -V -A)",
              r"-l (trees.VFDTDecay -D 0.9 -V -A)",
              #r"-l (trees.VFDTDecay -D 0.85 -V -A)",
              r"-l (trees.VFDTDecay -D 0.8 -V -A)",
              #r"-l (trees.VFDTDecay -D 0.75 -V -A)",
              r"-l (trees.VFDTDecay -D 0.7 -V -A)",
              r"-l (trees.VFDTDecay -D 0.6 -V -A)",
              r"-l (trees.VFDTDecay -D 0.5 -V -A)",
              r"-l (trees.VFDTDecay -D 0.4 -V -A)",
              r"-l (trees.VFDTDecay -D 0.3 -V -A)",

              r"-l (trees.VFDTDecay -D 0.99999 -A)",
              r"-l (trees.VFDTDecay -D 0.9999 -A)",
              r"-l (trees.VFDTDecay -D 0.999 -A)",
              r"-l (trees.VFDTDecay -D 0.99 -A)",
               r"-l (trees.VFDTDecay -D 0.8 -A)",
              r"-l (trees.VFDTDecay -D 0.7 -A)",
              r"-l (trees.VFDTDecay -D 0.6 -A)",
              r"-l (trees.VFDTDecay -D 0.5 -A)",
              r"-l (trees.VFDTDecay -D 0.3 -A)",

              r"-l (trees.VFDTDecay -D 0.99999 -V)",
              r"-l (trees.VFDTDecay -D 0.9999 -V)",
              r"-l (trees.VFDTDecay -D 0.999 -V)",
              r"-l (trees.VFDTDecay -D 0.99 -V)",
              r"-l (trees.VFDTDecay -D 0.9  -V)",
              r"-l (trees.VFDTDecay -D 0.7 -V)",
              r"-l (trees.VFDTDecay -D 0.6 -V)",
              r"-l (trees.VFDTDecay -D 0.5 -V)",
              r"-l (trees.VFDTDecay -D 0.3 -V)",


              
              #r"-l (trees.CVFDT -f 10000 -L 200 -W 400000)",
              #r"-l (trees.CVFDT -f 10000 -L 200 -W 200000)",
              #r"-l (trees.CVFDT -f 10000 -L 200 -W 100000)",
              #r"-l (trees.CVFDT -f 10000 -L 200 -W 50000)",
              #r"-l (trees.CVFDT -f 10000 -L 200 -W 25000)",
              #r"-l (trees.CVFDT -f 10000 -L 200 -W 10000)",
              #r"-l (trees.CVFDT -f 10000 -L 200 -W 5000)",

              #r"-l (trees.CVFDT -f 1000 -L 200 -W 400000)",
              #r"-l (trees.CVFDT -f 1000 -L 200 -W 200000)",
              #r"-l (trees.CVFDT -f 1000 -L 200 -W 100000)",
              #r"-l (trees.CVFDT -f 1000 -L 200 -W 50000)",
              #r"-l (trees.CVFDT -f 1000 -L 200 -W 25000)",
              #r"-l (trees.CVFDT -f 1000 -L 200 -W 10000)",
              #r"-l (trees.CVFDT -f 1000 -L 200 -W 5000)",

		r"-l trees.HATADWIN",
              r"-l (drift.SingleClassifierDrift -l trees.VFDT -d ADWINMonotoneChangeDetector)",
        ]
 
